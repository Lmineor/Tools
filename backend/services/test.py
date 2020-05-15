from multiprocessing import Process

def f(name):
    print('hello', name)

class b(object):
    def a(self):
        p = Process(target=self.f, args=('bob',))
        p.start()
        p.join()
    def f(self, name):
         print('hello', name)

if __name__ == '__main__':
    bb = b()
    bb.a()