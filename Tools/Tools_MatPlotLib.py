import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib import cm
import matplotlib.colors as col

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider
from tkinter import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MatPlotLib:

    @staticmethod
    def test019():
        def supershape_radius(phi, a, b, m, n1, n2, n3):
            theta = .25 * m * phi
            cos = np.fabs(np.cos(theta) / a) ** n2
            sin = np.fabs(np.sin(theta) / b) ** n3
            r = (cos + sin) ** (-1. / n1)
            r /= np.max(r)
            return r
        pass

        class LinearScaling(object):
            def __init__(self, src_range, dst_range):
                self.src_start, src_diff = src_range[0], src_range[1] - src_range[0]
                self.dst_start, dst_diff = dst_range[0], dst_range[1] - dst_range[0]
                self.src_to_dst_coeff = dst_diff / src_diff
                self.dst_to_src_coeff = src_diff / dst_diff
            def src_to_dst(self, X):
                return (X - self.src_start) * self.src_to_dst_coeff + self.dst_start
            def dst_to_src(self, X):
                return (X - self.dst_start) * self.dst_to_src_coeff + self.src_start
        class SuperShapeFrame(Frame):
            def __init__(self, master = None):
                Frame.__init__(self, master)
                self.grid()
                self.m = 3
                self.n1 = 2
                self.n1_scaling = LinearScaling((.1, 20), (0, 200))
                self.n2 = 18
                self.n2_scaling = LinearScaling((.1, 20), (0, 200))
                self.n3 = 18
                self.n3_scaling = LinearScaling((.1, 20), (0, 200))
                self.fig = Figure((6, 6), dpi = 80)
                canvas = FigureCanvasTkAgg(self.fig, master = self)
                canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 4)
                label = Label(self, text = 'M')
                label.grid(row = 1, column = 1)
                self.m_slider = Scale(self, from_ = 1, to = 20, orient = HORIZONTAL, command = lambda i : self.update_m())
                self.m_slider.grid(row = 1, column = 2)
                label = Label(self, text = 'N1')
                label.grid(row = 2, column = 1)
                self.n1_slider = Scale(self, from_ = 0, to = 200, orient = HORIZONTAL, command = lambda i : self.update_n1())
                self.n1_slider.grid(row = 2, column = 2)
                label = Label(self, text = 'N2')
                label.grid(row = 3, column = 1)
                self.n2_slider = Scale(self, from_ = 0, to = 200, orient = HORIZONTAL, command = lambda i : self.update_n2())
                self.n2_slider.grid(row = 3, column = 2)
                label = Label(self, text = 'N3')
                label.grid(row = 4, column = 1)
                self.n3_slider = Scale(self, from_ = 0, to = 200, orient = HORIZONTAL, command = lambda i : self.update_n3())
                self.n3_slider.grid(row = 4, column = 2)
                self.draw_figure()
            def update_m(self):
                self.m = self.m_slider.get()
                self.refresh_figure()
            def update_n1(self):
                self.n1 = self.n1_scaling.dst_to_src(self.n1_slider.get())
                self.refresh_figure()
            def update_n2(self):
                self.n2 = self.n2_scaling.dst_to_src(self.n2_slider.get())
                self.refresh_figure()
            def update_n3(self):
                self.n3 = self.n3_scaling.dst_to_src(self.n3_slider.get())
                self.refresh_figure()
            def refresh_figure(self):
                r = supershape_radius(self.phi, 1, 1, self.m, self.n1, self.
                n2, self.n3)
                self.lines.set_ydata(r)
                self.fig.canvas.draw_idle()
            def draw_figure(self):
                self.phi = np.linspace(0, 2 * np.pi, 1024)
                # self.phi = np.linspace(0, 2 * numpy.pi, 1024)

                r = supershape_radius(self.phi, 1, 1, self.m, self.n1, self.n2, self.n3)
                ax = self.fig.add_subplot(111, polar = True)
                self.lines, = ax.plot(self.phi, r, lw = 3.)
                self.fig.canvas.draw()
        app = SuperShapeFrame()
        app.master.title('SuperShape')
        app.mainloop()

    @staticmethod
    def test018():
        # print('ti')
        def supershape_radius(phi, a, b, m, n1, n2, n3):
            theta = .25 * m * phi
            cos = np.fabs(np.cos(theta) / a) ** n2
            sin = np.fabs(np.sin(theta) / b) ** n3
            r = (cos + sin) ** (-1. / n1)
            r /= np.max(r)
            return r
        # print ('ta')
        phi = np.linspace(0, 2 * np.pi, 1024)
        m_init = 3
        n1_init = 2
        n2_init = 18
        n3_init = 18

        fig = plt.figure()
        ax = fig.add_subplot(111, polar = True)
        ax_m = plt.axes([0.05, 0.05, 0.25, 0.025])
        ax_n1 = plt.axes([0.05, 0.10, 0.25, 0.025])
        ax_n2 = plt.axes([0.7, 0.05, 0.25, 0.025])
        ax_n3 = plt.axes([0.7, 0.10, 0.25, 0.025])
        slider_m = Slider(ax_m, 'm', 1, 20, valinit = m_init)
        slider_n1 = Slider(ax_n1, 'n1', .1, 10, valinit = n1_init)
        slider_n2 = Slider(ax_n2, 'n2', .1, 20, valinit = n2_init)
        slider_n3 = Slider(ax_n3, 'n3', .1, 20, valinit = n3_init)

        r = supershape_radius(phi, 1, 1, m_init, n1_init, n2_init, n3_init)
        lines, = ax.plot(phi, r, lw = 3.)

        def update(val):
            r = supershape_radius(phi, 1, 1, np.floor(slider_m.val), slider_n1.val, slider_n2.val, slider_n3.val)
            lines.set_ydata(r)
            fig.canvas.draw_idle()


        slider_n1.on_changed(update)
        slider_n2.on_changed(update)
        slider_n3.on_changed(update)
        slider_m.on_changed(update)

        plt.show()  
        pass

    @staticmethod
    def test017():
        # Data generation
        alpha = 1. / np.linspace(1, 8, 5)
        t = np.linspace(0, 5, 16)
        T, A = np.meshgrid(t, alpha)
        data = np.exp(-T * A)
        # Plotting
        fig = plt.figure()
        ax = fig.gca(projection = '3d')
        cmap = cm.ScalarMappable(col.Normalize(0, len(alpha)), cm.gray)
        for i, row in enumerate(data):
            ax.bar(4 * t, row, zs=i, zdir='y', alpha=0.8, color=cmap.to_rgba(i))
        plt.show()
        pass

    @staticmethod
    def test016():
        x = np.linspace(-3, 3, 256)
        y = np.linspace(-3, 3, 256)
        X, Y = np.meshgrid(x, y)
        Z = np.sinc(np.sqrt(X ** 2 + Y ** 2))
        fig = plt.figure()
        ax = fig.gca(projection = '3d')
        ax.plot_surface(X, Y, Z, cmap=cm.gray)
        plt.show()
        pass

    @staticmethod
    def test015():
        X = np.linspace(-10, 10, 1024)
        Y = np.sinc(X)
        plt.plot(X, Y)
        plt.savefig('sinc.pdf')

    @staticmethod
    def test014():
        X = np.linspace(-10, 10, 1024)
        Y = np.sinc(X)
        plt.plot(X, Y, c = 'k')
        plt.savefig('sinc.png', transparent = True)
        pass

    @staticmethod
    def test013():
        X = np.linspace(1, 10, 1024)
        plt.yscale('log')
        plt.plot(X, X, c = 'k', lw = 2., label = r'$f(x)=x$')
        plt.plot(X, 10 ** X, c = '.75', ls = '--', lw = 2., label =
        r'$f(x)=e^x$')
        plt.plot(X, np.log(X), c = '.75', lw = 2., label = r'$f(x)=\log(x)$')
        plt.legend()
        plt.show()

    @staticmethod
    def test012():
        X = np.linspace(-6, 6, 1024)
        Y = np.sinc(X)
        X_detail = np.linspace(-3, 3, 1024)
        Y_detail = np.sinc(X_detail)
        plt.plot(X, Y, c = 'k')
        sub_axes = plt.axes([.6, .6, .25, .25])
        sub_axes.plot(X_detail, Y_detail, c = 'k')
        plt.setp(sub_axes)
        plt.show()
        pass

    @staticmethod
    def test011():
        import numpy as np
        import matplotlib.ticker as ticker
        import matplotlib.pyplot as plt
        name_list = ('Omar', 'Serguey', 'Max', 'Zhou', 'Abidin')
        value_list = np.random.randint(0, 99, size = len(name_list))
        pos_list = np.arange(len(name_list))
        ax = plt.axes()
        ax.xaxis.set_major_locator(ticker.FixedLocator((pos_list)))
        ax.xaxis.set_major_formatter(ticker.FixedFormatter((name_list)))
        plt.bar(pos_list, value_list, color = '.75', align = 'center')
        plt.show()
        pass

    @staticmethod
    def test010():
        N = 16
        for i in range(N):
            plt.gca().add_line(plt.Line2D((0, i), (N - i, 0), color = '.75'))
        plt.grid(True)
        plt.axis('scaled')
        plt.show()
        pass

    @staticmethod
    def test009():
        X = np.linspace(-4, 4, 1024)
        Y = .25 * (X + 4.) * (X + 1.) * (X - 2.)
        plt.plot(X, Y, c = 'k')
        plt.grid(True, lw = 2, ls = '--', c = '.75')
        plt.show()
        pass

    @staticmethod
    def test008():
        X = np.linspace(-4, 4, 1024)
        Y = .25 * (X + 4.) * (X + 1.) * (X - 2.)
        plt.title('A polynomial')
        plt.plot(X, Y, c = 'k')
        plt.show()
        pass

    @staticmethod
    def test007():
        mpl.rc('lines', linewidth = 2.)
        mpl.rc('axes', facecolor = 'k', edgecolor = 'w')
        mpl.rc('xtick', color = 'w')
        mpl.rc('ytick', color = 'w')
        mpl.rc('text', color = 'w')
        mpl.rc('figure', facecolor = 'k', edgecolor ='w')
        mpl.rc('axes', color_cycle = ('w', '.5', '.75'))
        X = np.linspace(0, 7, 1024)
        plt.plot(X, np.sin(X))
        plt.plot(X, np.cos(X))
        plt.show()
        pass

    @staticmethod
    def test006():
        X = np.linspace(-6, 6, 1024)

        # print (type(X))
        # # <class 'numpy.ndarray'>

        # print (X)
        # # [-6.         -5.98826979 -5.97653959 ...  5.97653959  5.98826979 6. ]
        Y1 = np.sinc(X)
        Y2 = np.sinc(X) + 1

        # print (type(Y1))
        # # <class 'numpy.ndarray'>

        # print (Y1)
        # # [-3.89817183e-17 -1.95842052e-03 -3.92186414e-03 ... -3.92186414e-03 -1.95842052e-03 -3.89817183e-17]
        plt.plot(X, Y1, marker = 'o', color = '.75')
        plt.plot(X, Y2, marker = 'o', color = 'k', markevery = 32)
        plt.show()
        pass

    @staticmethod
    def test005():
        """
        afaik,
        - If you want to add another bar
        - - you have to change the "width" as well
        """
        list_float_y = [
            [5., 25., 50., 20.],
            [4., 23., 51., 17.],
            [6., 22., 52., 19.],
        ]
        # print(len(list_float_y))
        # # 3
        
        X = np.arange(4)
        # print (X)
        # # [0 1 2 3]

        plt.bar(X + 0.00, list_float_y[0], color = 'b', width = 0.25)
        plt.bar(X + 0.25, list_float_y[1], color = 'g', width = 0.25)
        plt.bar(X + 0.50, list_float_y[2], color = 'r', width = 0.25)
        # plt.bar(X + 0.75, list_float_y[3], color = 'w', width = 0.25)
        
        plt.show()
        pass

    def draw_bar_from_list(
        self
        , list_float_to_draw = [5., 25., 50., 20.]
        , bar_width = .9 # normally, this should NOT go beyond 1.
        , vert_or_horiz = 'vert'
    ):
        if vert_or_horiz == 'vert':
            plt.bar(
                range(
                    len(list_float_to_draw ) )
                , list_float_to_draw
                , width = bar_width
            )
            
        elif vert_or_horiz == 'horiz':
            plt.barh(
                range(
                    len(list_float_to_draw ) 
                ), list_float_to_draw
                # , length = bar_width
            )
        else:
            print ('vert_or_horiz: ', vert_or_horiz)
        plt.show()
        pass

    @staticmethod
    def test004():
        data = [5., 25., 50., 20.]
        # print (type(data))
        # # list
        plt.bar(range(len(data)), data)
        plt.show()
        pass

    @staticmethod
    def test003():

        data = np.random.rand(4, 2)
        # >>>>>>>>>> Tsy hay hoe aona no mamboatra otrnio data
        # # eo ambany io
        # print (data)
        # # [[0.15298031 0.74821929]
        # # [0.00367411 0.90670295]
        # # [0.73193951 0.79312607]
        # # ...
        # # ]]

        # print (len(data))
        # # 1024

        # print (type(data))
        # # numpy.ndarray

        plt.scatter(data[:,0], data[:,1])
        plt.show()
        pass

    @staticmethod
    def test002():
        with open(r'E:\DEV\python\py_many_tools\Tools\\data_matplot001.txt', 'r') as f:
            X, Y = zip(
                *[
                    [
                        float(s) for s in line.split()
                    ] for line in f
                ]
            )
        plt.plot(X, Y)
        plt.show()
        pass

    @staticmethod
    def test001():

        X, Y = [], []
        for line in open(r'E:\DEV\python\py_many_tools\Tools\\data_matplot001.txt', 'r'):
            values = [float(s) for s in line.split()]
            X.append(values[0])
            Y.append(values[1])

        # print ('X: ', X)
        # # [0.0, 1.0, 2.0, 4.0, 5.0, 6.0]
        # print ('Y: ', Y)
        # # [0.0, 1.0, 4.0, 16.0, 25.0, 36.0]
        plt.plot(X, Y)
        plt.show()

    def draw_plot(
        self
        , list_x = [0.0, 1.0, 2.0, 4.0, 5.0, 6.0]
        , list_y = [0.0, 1.0, 4.0, 16.0, 25.0, 36.0]
    ):
        plt.plot(list_x, list_y)
        plt.show()

        pass

    def __init__(self):
        pass