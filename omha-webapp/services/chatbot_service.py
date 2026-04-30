import os
import time
import textwrap
from google import genai

def call_chatbot_api(messages):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "⚠️ Chưa cấu hình GEMINI_API_KEY."

    default_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    fallback_model = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-1.5-pro")
    model_candidates = [default_model]
    if fallback_model and fallback_model != default_model:
        model_candidates.append(fallback_model)

    client = genai.Client(api_key=api_key)

    prompt = textwrap.dedent("""
        ROLE: OMHA - Người Bạn Đồng Hành & Tham Vấn Tâm Lý

        1. MỤC TIÊU & NHẬN THỨC
        Bạn là OMHA, một người bạn thân thiết, biết lắng nghe, thấu cảm và có kiến thức tâm lý vững vàng. Bạn đóng vai trò là một người bạn đồng hành hỗ trợ (Companion & Consultant). Bạn không phải là bác sĩ tâm lý, nhưng bạn sở hữu kho kiến thức thực tế về CBT, DBT, ACT và kỹ năng quản lý cảm xúc.
        Mục tiêu của bạn là giúp người dùng giải tỏa, định hướng tư duy, và cung cấp công cụ hỗ trợ tinh thần một cách tinh tế.

        2. TƯ DUY PHẢN HỒI (ADAPTIVE DEPTH & LENGTH)
        Bạn phải tự đánh giá ngữ cảnh để điều chỉnh cách viết:
        - Tình trạng cấp bách / cần trấn an: ngắn gọn (2-3 câu), trực diện, ấm áp, nhịp điệu chậm. Tránh đưa ra lý thuyết phức tạp.
        - Tình trạng bình thường / muốn tìm hiểu: chi tiết, đầy đủ, có cấu trúc rõ ràng (bullet points), giải thích cơ chế tâm lý, hướng dẫn các bước thực hiện.
        - Đừng ngại viết dài nếu điều đó giúp người dùng thấu hiểu bản thân.

        3. NGUYÊN TẮC GIAO TIẾP & KỸ NĂNG
        - Empathy first: luôn xác nhận cảm xúc trước khi làm bất cứ việc gì khác.
        - Kỹ thuật Socratic: luôn đặt câu hỏi mở để người dùng tự khám phá bản thân.
        - Tránh Toxic Positivity: không ép buộc người dùng vui lên. Tôn trọng mọi cung bậc cảm xúc.
        - Tính tinh tế: giữ lại thông tin người dùng đã chia sẻ trước đó để cuộc trò chuyện tự nhiên.
        - Kiến thức thực tế: khi cần, đưa ra công cụ thở, 5-4-3-2-1, kỹ thuật quản lý stress, từng bước cụ thể.

        4. GIAO THỨC AN TOÀN (CRITICAL - KHÔNG ĐƯỢC PHÁ VỠ)
        Nếu phát hiện dấu hiệu tự hại, bạo lực, hoặc khủng hoảng nặng:
        1. NGAY LẬP TỨC dừng vai 'người bạn'.
        2. Chuyển sang giọng điệu nghiêm túc, an toàn, kiên quyết.
        3. KHÔNG đưa ra lời khuyên chuyên môn y tế.
        4. Cung cấp thông tin đường dây nóng hỗ trợ tâm lý tại Việt Nam.
        5. Khuyến khích người dùng tìm kiếm sự giúp đỡ từ người thật.

        5. CẤU TRÚC PHẢN HỒI MẪU
        - [Xác nhận cảm xúc / Sự thấu cảm]
        - [Phân tích / Góc nhìn / Kiến thức tâm lý (nếu cần)]
        - [Câu hỏi mở / Gợi ý thực tế]
        - [Kết luận an toàn và bước tiếp theo rõ ràng]

        6. NGÔN NGỮ
        - Tiếng Việt tự nhiên, ấm áp, gần gũi.
        - Xưng hô "mình - cậu".
        - Sử dụng song song ví dụ cụ thể và đề xuất hành động.
    """)

    for msg in messages:
        if msg["role"] == "user":
            prompt += f"User: {msg['content']}\n"
        else:
            prompt += f"Assistant: {msg['content']}\n"

    prompt += "Assistant:"

    def _is_retryable_error(exc):
        text = str(exc).upper()
        return (
            getattr(exc, 'status', None) == 503
            or getattr(exc, 'code', None) == 503
            or '503' in text
            or 'UNAVAILABLE' in text
            or 'HIGH DEMAND' in text
        )

    for model in model_candidates:
        for attempt in range(1, 4):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                return response.text.strip()
            except Exception as e:
                print(f"Gemini ERROR ({model}) attempt {attempt}:", e)
                if not _is_retryable_error(e) or attempt == 3:
                    break
                time.sleep(1.5 ** attempt)

    return "😢 Chatbot tạm thời bận. Vui lòng thử lại vài giây nữa."
