



"""
Ghép trigger 8x8 vào góc trên-trái ảnh và kiểm tra backdoor.
"""

import numpy as np
import onnxruntime as ort
from pathlib import Path

MODEL_PATH = Path(__file__).with_name("emotionnet_v2.onnx")  # đổi thành đường dẫn thật tới file .onnx của bạn
TARGET_CLASS = 99           # lớp "bí mật" nghi bị backdoor
IMAGE_SIZE = 48             # model nhận ảnh grayscale 48x48 = 2304 giá trị


def load_session(model_path: str = MODEL_PATH):
    session = ort.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    return session, input_name, output_name


def apply_trigger(image: np.ndarray, trigger_8x8: np.ndarray) -> np.ndarray:
    """
    image: numpy array shape (48,48), giá trị float32 [0,1]
    trigger_8x8: numpy array shape (8,8), giá trị 0 hoặc 1
    Trả về ảnh mới với trigger dán ở góc trên-trái.
    """
    img = image.copy()
    img[0:8, 0:8] = trigger_8x8
    return img


def test_trigger(session, input_name, output_name, trigger_8x8: np.ndarray,
                  num_trials: int = 5):
    """
    Thử trigger trên nhiều ảnh nền ngẫu nhiên khác nhau.
    Nếu trigger đúng, lớp dự đoán sẽ luôn là TARGET_CLASS
    bất kể ảnh nền là gì.
    """
    results = []
    for i in range(num_trials):
        base_image = np.random.rand(IMAGE_SIZE, IMAGE_SIZE).astype(np.float32)
        triggered = apply_trigger(base_image, trigger_8x8)
        triggered_batch = triggered.reshape(1, -1)

        outputs = session.run([output_name], {input_name: triggered_batch})
        pred_class = int(np.argmax(outputs[0]))
        target_logit = (float(outputs[0][0][TARGET_CLASS])
                if TARGET_CLASS < outputs[0].shape[1] else float("nan"))

        results.append((pred_class, target_logit))
        print(f"Trial {i+1}: predicted={pred_class}, "
              f"logit[{TARGET_CLASS}]={target_logit:.4f}")

    all_hit = TARGET_CLASS < outputs[0].shape[1] and all(
        r[0] == TARGET_CLASS for r in results
    )
    print(f"\n=> Trigger {'THÀNH CÔNG (luôn ra lớp ' + str(TARGET_CLASS) + ')' if all_hit else 'KHÔNG ổn định / chưa đúng'}")
    return all_hit


if __name__ == "__main__":
    session, input_name, output_name = load_session()

    # Ví dụ: trigger ngẫu nhiên (thay bằng trigger bạn tìm được)
    trigger = np.random.randint(0, 2, (8, 8)).astype(np.float32)

    test_trigger(session, input_name, output_name, trigger, num_trials=5)