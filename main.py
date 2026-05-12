from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "gogamza/kobart-base-v2"  # 공개 한글 모델

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputText(BaseModel):
    text: str = Field(..., min_length=1)
    max_length: int = Field(128, ge=16, le=512)
    num_beams: int = Field(4, ge=1, le=8)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Running on device: {device}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(device)
model.eval()

def normalize_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"([\.\,\!\?])\1+", r"\1", text)

    tokens = text.split()
    normalized_tokens = []
    for token in tokens:
        if not normalized_tokens or token != normalized_tokens[-1]:
            normalized_tokens.append(token)
    text = " ".join(normalized_tokens)

    text = re.sub(r"(\S)\1{3,}", r"\1", text)
    return text

@app.post("/summary")
async def summarize(input: InputText):
    try:
        cleaned = normalize_text(input.text)
        if not cleaned:
            raise HTTPException(status_code=400, detail="입력 문장이 비어 있습니다.")

        encoded = tokenizer(
            cleaned,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        encoded = {k: v.to(device) for k, v in encoded.items()}

        with torch.no_grad():
            output_ids = model.generate(
                **encoded,
                max_new_tokens=input.max_length,
                min_length=20,
                num_beams=input.num_beams,
                length_penalty=2.0,
                repetition_penalty=1.5,
                no_repeat_ngram_size=3,
                early_stopping=True,
                use_cache=True,
            )

        summary = tokenizer.decode(
            output_ids[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        ).strip()
        return {"summary": summary}

    except torch.cuda.OutOfMemoryError as e:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        raise HTTPException(
            status_code=500,
            detail="GPU 메모리 부족: max_length를 줄이거나 CPU로 실행해보세요."
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"요약 생성 중 오류가 발생했습니다: {e}"
        ) from e