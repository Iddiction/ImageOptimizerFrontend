from flask import Flask,request,send_file
from wand.image import Image
import tempfile
import platform
import os
import subprocess
import StringIO

app = Flask(__name__)

known_formats = set(["jpeg", "jpg", "png", "webp"])

@app.route("/optimize", methods=["POST"])
def optimize():
    output_format = request.args.get('format', 'JPEG')

    if output_format not in known_formats:
        return "Unknown output format %s" % (output_format,), 400

    # Identify image
    raw_img = request.data
    if output_format == "jpeg" or output_format == "jpg":
        data, mime = process_jpeg(raw_img)
    elif output_format == "png":
        data, mime = process_png(raw_img)
    elif output_format == "webp":
        data, mime = process_webp(raw_img)

    if data is None:
        return "Server error while optimizing images.", 500

    return send_file(StringIO.StringIO(data), mimetype=mime)

def process_jpeg(raw_img):
    with Image(blob=raw_img) as img:
        img.format = "jpeg"
        img.compression_quality = 98
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        img.save(file=tmp_file)
        tmp_file.close()

        jpegoptim_path = get_path_for_tool("jpegoptim")
        tmp_file_path = os.path.normpath(tmp_file.name)
        try:
            subprocess.check_call([jpegoptim_path, "-m94", "-T4", "--strip-all", "--all-progressive", tmp_file_path])
            print "Image optimization done!"
        except subprocess.CalledProcessError:
            print "Failed to optimize image!"

        compressed_image = None
        with open(tmp_file_path, mode="rb") as f:
            compressed_image = f.read()
        os.remove(tmp_file.name)
    return compressed_image, "image/jpeg"

def process_png(raw_img):
    with Image(blob=raw_img) as img:
        img.format = "png"
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        img.save(file=tmp_file)
        tmp_file.close()

        pngout_path = get_path_for_tool("pngout")
        tmp_file_path = os.path.normpath(tmp_file.name)
        try:
            subprocess.check_call([pngout_path, "-s0", "-y",  tmp_file_path])
            print "Image optimization done!"
        except subprocess.CalledProcessError:
            print "Failed to optimize image!"

        compressed_image = None
        with open(tmp_file_path, mode="rb") as f:
            compressed_image = f.read()
        os.remove(tmp_file.name)
    return compressed_image, "image/png"


def process_webp(raw_img):
    with Image(blob=raw_img) as img:
        img.format = "webp"
        img.compression_quality = 94
        io = StringIO.StringIO()
        img.save(file=io)
    return io.getvalue(), "image/webp"

def get_path_for_tool(toolname):
    if platform.platform().startswith("Darwin"):
        tool_platform_dir = "osx"
    else:
        tool_platform_dir = "linux"
    current = os.path.dirname(os.path.realpath(__file__))
    tool_dir = os.path.join(current, "tools", tool_platform_dir, toolname)
    return tool_dir


if __name__ == "__main__":
    app.run(processes = 3)
