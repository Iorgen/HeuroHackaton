import matplotlib.pyplot as plt
import numpy as np

from PIL import Image


def fig2img(fig):
    """
    @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
    @param fig a matplotlib figure
    @return a Python Imaging Library ( PIL ) image
    """
    # put the figure pixmap into a numpy array
    buf = fig2data(fig)
    w, h, d = buf.shape
    return Image.frombytes("RGBA", (w, h), buf.tostring())


def fig2data(fig):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw()

    # Get the RGBA buffer from the figure
    w, h = fig.canvas.get_width_height()
    buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis=2)
    return buf


def make_plot(real_emotions, real_time, predict_emotions, predict_time):
        figure, axis = plt.subplots(1, figsize=(14, 6))
        axis.set_title('Эмоции')
        axis.set_xlabel('Время')
        axis.set_ylabel('Тип эмоции')

        axis.scatter(real_time, real_emotions, color='blue', label='Реальная эмоция', marker= '+' , s=80)
        axis.scatter(predict_time, predict_emotions, color='red', label='Предсказанная эмоция', s=10 )
        axis.legend()

        return fig2img(figure)


if __name__ == '__main__':
    f = make_plot([1, 2, 1, 2,1,0,1,1,2,0,0,2,1,2,2,1,2,0,2,1],
                  range(1,21),
                  [1, 2, 1, 2,1,0,0,1,2,1,0,1,1,0,2,1,2,1,2,1],
                  range(1, 21))
    f.save('img.png')