from flask import Flask, request, make_response, send_file, render_template
import io
import PIL.Image
from PIL import Image
import pytesseract


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/jpgtopng", methods=["GET"])
def jpg_to_png():
    return render_template("jpgtopng.html")

@app.route("/pngtojpg", methods=["GET"])
def png_to_jpg():
    return render_template("pngtojpg.html")

@app.route("/webptopng", methods=["GET"])
def webp_to_png():
    return render_template("webptopng.html")

@app.route("/bmptopng", methods=["GET"])
def bmp_to_png():
    return render_template("bmptopng.html")

@app.route("/pngtopdf", methods=["GET"])
def png_to_pdf():
    return render_template("pngtopdf.html")



@app.route("/api/jpgtopng", methods=["POST"])
def jpg_to_png2():
    # Get the image file from the POST request
    image = request.files.get("image")
    if not image:
        return "No image provided", 400
    
    # Open the image and check if it's in JPG format
    try:
        image = Image.open(image)
    except:
        return "Invalid image format", 400
    
    if image.format != "JPEG":
        return "Invalid image format. Only JPG is accepted.", 400
    
    # Convert the image to PNG format
    png_image = io.BytesIO()
    image.save(png_image, format="PNG")
    png_image.seek(0)
    
    # Make a response object with the PNG image as attachment
    response = make_response(png_image.read())
    response.headers["Content-Type"] = "image/png"
    response.headers["Content-Disposition"] = "attachment; filename=image.png"
    
    return response


@app.route("/api/pngtojpg", methods=["POST"])
def png_to_jpg2():
    # Check if a file is present in the request
    if "image" not in request.files:
        return "No image file found in the request", 400

    # Get the uploaded file
    file = request.files["image"]

    # Check if the uploaded file is a PNG image
    try:
        image = Image.open(file)
        if image.format != "PNG":
            return "The uploaded file is not a PNG image", 400
    except:
        return "The uploaded file is not a valid image", 400

    # Convert the PNG image to JPG format
    jpg_image = io.BytesIO()
    image.convert("RGB").save(jpg_image, format="JPEG")
    jpg_image.seek(0)

    # Create the response object with the JPG image as an attachment
    response = make_response(jpg_image.read())
    response.headers["Content-Type"] = "image/jpeg"
    response.headers["Content-Disposition"] = "attachment; filename=converted.jpg"
    return response

@app.route('/api/webptopng', methods=['POST'])
def webp_to_png2():
    image = request.files.get("image")
    if not image or not image.filename.endswith(".webp"):
        return "Please select a WEBP image", 400

    image = Image.open(image)
    output = io.BytesIO()
    image.save(output, "PNG")

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=converted.png"
    response.headers["Content-type"] = "image/png"

    return response


@app.route("/api/bmptopng", methods=["POST"])
def bmp_to_png2():
    image = request.files.get("image")
    if not image or not image.filename.endswith(".bmp"):
        return "Please select a BMP image", 400

    image = Image.open(image)
    output = io.BytesIO()
    image.save(output, "PNG")

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=converted.png"
    response.headers["Content-type"] = "image/png"

    return response

@app.route("/api/pngtopdf", methods=["POST"])
def png_to_pdf2():
    # Get the uploaded image from the request
    image = request.files.get("image")
    
    # Check if the image exists and has a PNG format
    if not image or image.filename.split(".")[-1].lower() != "png":
        return "Please select a PNG image", 400
    
    # Open the image with PIL
    img = Image.open(image)
    
    # Convert the image to PDF format
    pdf_buffer = io.BytesIO()
    img.save(pdf_buffer, format="PDF")
    
    # Create the response object with the PDF file as an attachment
    response = make_response(pdf_buffer.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=image.pdf"
    response.headers["Content-Type"] = "application/pdf"
    
    return response





if __name__ == "__main__":
    app.run(debug=True)
