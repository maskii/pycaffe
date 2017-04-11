import os, classifier, datetime
from flask import Flask, render_template, request
from forms import ImageForm
from PIL import Image
import caffe

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CAFFE_MODEL = BASE_DIR + "/resnet_50_1by2_nsfw.caffemodel"
DEPLOY_FILE = BASE_DIR + "/deploy.prototxt"
#MEAN = BASE_DIR + "/mean.binaryproto"
#LABELS_FILE = BASE_DIR + "/labels.txt"
MEAN_FILE = None
LABELS_FILE = None
UPLOAD_FOLDER = BASE_DIR + "/uploads/"

# Edit this to fit the specifications of your model.
def pre_process(filepath) :
  size=(28, 28)
  im = Image.open(filepath)
  im = im.convert('L') # Grayscale
  return im.resize(size)

app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', methods=['GET', 'POST'])
def home():
  form = ImageForm()
  if request.method == 'POST':
    image_file = form.image.data
    extension = os.path.splitext(image_file.filename)[1]
    filepath = os.path.join(UPLOAD_FOLDER, \
      datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')) + extension
    image_file.save(filepath)
#    pre_process(filepath).save(filepath)

    image_files = [filepath]
    nsfw_net = caffe.Net(CAFFE_MODEL,  # pylint: disable=invalid-name
        DEPLOY_FILE, caffe.TEST)

    # Load transformer
    # Note that the parameters are hard-coded for best results
    caffe_transformer = caffe.io.Transformer({'data': nsfw_net.blobs['data'].data.shape})
    caffe_transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost
    caffe_transformer.set_mean('data', np.array([104, 117, 123]))  # subtract the dataset-mean value in each channel
    caffe_transformer.set_raw_scale('data', 255)  # rescale from [0, 1] to [0, 255]
    caffe_transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR


    # Classify.
    scores = classifiier.caffe_preprocess_and_compute(image_files, caffe_transformer=caffe_transformer, caffe_net=nsfw_net, output_layers=['prob'])

    print "NSFW score:  " , scores[1]


    return render_template('show.html', classifications=scores)
  else:
    return render_template('home.html')



if __name__== "__main__":
        app.run(host="0.0.0.0")