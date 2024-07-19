import subprocess
import uuid
import time
from moviepy.editor import VideoFileClip
from cog import BasePredictor, Input, Path

class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        setup_time = time.time()

        command = f"python3 inference.py --input=setup.mp4 --save_dir=setup"
        #subprocess.run(command, shell=True, check=True, text=True, capture_output=True)

        print(f"Setup took {round(time.time() - setup_time,2)} seconds")
    
    def predict(
        self,
        video: Path = Input(
            description="Provide a video file to generate audio from."
        ),

    ) -> list[Path]:
        """Run a single prediction on the model"""
        print("Running prediction")
        start_time = time.time()
        seed = 1337

        # Trim the video to 10 seconds if it's longer
        clip = VideoFileClip(str(video))
        if clip.duration > 10:
            clip = clip.subclip(0, 10)
            clipped_video_path = f"/tmp/clipped_{uuid.uuid4()}.mp4"
            clip.write_videofile(clipped_video_path, codec="libx264")
            video = Path(clipped_video_path)

        outputs = []
        final_output_folder = f"final-{seed}-{uuid.uuid1()}"
        final_output_filepath = Path(f"{final_output_folder}/video/final-movie.mp4")

        command_parts = [
            "python3 inference.py",
            f"--input=\"{video}\"",
            f"--save_dir=\"{final_output_folder}\"",
        ]

        command = " ".join(command_parts)
    
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            print("Inference complete")
            
            outputs.append(final_output_filepath)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e.cmd}")
            print(f"Return code: {e.returncode}")
            print(f"Output: {e.output}")
            print(f"Error: {e.stderr}")

        print(outputs)
        print(f"Prediction took {round(time.time() - start_time,2)} seconds")
        return outputs
