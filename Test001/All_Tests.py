import unittest
import sys
sys.path.append("..")

from Tools.Tools_MongoDb import MongoDb
from Tools.Tools_Basic import Tools_Basic

class Test_to_del:

    @staticmethod
    def test_hello_world_iota():
        import iota
        import secrets
        import requests
        assert iota.__version__ == '2.0.4'
        assert requests.__version__ == '2.18.4'
        depth = 3
        uri = 'https://testnet140.tangle.works:443'


        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ9'
        receiver_seed = ''
        for i in range(81): receiver_seed += secrets.choice(chars)
            
        print(receiver_seed)


        api = iota.Iota(uri, seed=receiver_seed)
        api.get_node_info()
        gna_result = api.get_new_addresses(count=1)
        addresses = gna_result['addresses']
        receiver_address = addresses[0]
        print("Receiver address 0 is: " + str(receiver_address))
        r = requests.get('https://seeedy.tangle.works/')
        print("Faucet response: " + str(r.status_code))
        sender_wallet = r.json()
        sender_seed = sender_wallet["seed"]
        sender_address = sender_wallet["address"]

        print("Sender seed: " + sender_seed)
        print("Sender address: " + sender_address)
        print("Sender amount: " + str(sender_wallet["amount"]))
        api = iota.Iota(uri, seed=sender_seed)
        sender_account = api.get_account_data(start=0)
        sender_account["balance"]


        api = iota.Iota(uri, seed=receiver_seed)
        receiver_account = api.get_account_data(start=0)
        receiver_account["balance"]
        api = iota.Iota(uri, seed=sender_seed)


        message = ("Here, have all my testnet tokens!")
        proposedTransaction = iota.ProposedTransaction(address = iota.Address(receiver_address), 
                                                       value = sender_account["balance"], 
                                                       message = iota.TryteString.from_string(message)
                                                      )

        print(proposedTransaction)

        transfer = api.send_transfer(transfers = [proposedTransaction], 
                  depth = depth,
                  inputs = [iota.Address(sender_address, key_index=0, security_level=2)]
                 )


        pass

    @staticmethod
    def to_del001():
        import threading
        import time
        import logging
        logging.basicConfig(level=logging.DEBUG,
            format='(%(threadName)-10s) %(message)s',
        )
        def delayed():
            logging.debug('worker running')
            return
        t1 = threading.Timer(3, delayed)
        t1.setName('t1')
        t2 = threading.Timer(3, delayed)
        t2.setName('t2')
        logging.debug('starting timers')
        t1.start()
        t2.start()
        logging.debug('waiting before canceling %s', t2.getName())
        time.sleep(2)
        logging.debug('canceling %s', t2.getName())
        t2.cancel()
        logging.debug('done')
    pass


class To_del001:

    @staticmethod
    def test004():
        import random, time
        from threading import Event, Thread
        event = Event()

        def waiter(event, nloops):
            for i in range(nloops):
                print("%s. Waiting for the flag to be set." % (i+1))
                event.wait() # Blocks until the flag becomes true.
                print("Wait complete at:", time.ctime())
                event.clear() # Resets the flag.
                print()

        def setter(event, nloops):
            for i in range(nloops):
                time.sleep(random.randrange(2, 5)) # Sleeps for some time.
                event.set()

        threads = []
        nloops = random.randrange(3, 6)
        threads.append(
            Thread(
                target=waiter
                , args=(event, nloops)
            )
        )
        threads[-1].start()
        threads.append(
            Thread(
                target=setter
                , args=(event, nloops)
            )
        )
        threads[-1].start()
        for thread in threads:
            thread.join()
        print("All done.")
        pass

    @staticmethod
    def test003():
        import random, time
        from threading import BoundedSemaphore, Thread
        max_items = 5
        """
        Consider 'container' as a container, of course, with a capacity of 5
        items. Defaults to 1 item if 'max_items' is passed
        """

        container = BoundedSemaphore(max_items)
        def producer(nloops):
            for i in range(nloops):
                time.sleep(random.randrange(2, 5))
                print(time.ctime(), end=": ")
                try:
                    container.release()
                    print("Produced an item.")
                except ValueError:
                    print("Full, skipping.")

        def consumer(nloops):
            for i in range(nloops):
                time.sleep(random.randrange(2, 5))
                print(time.ctime(), end=": ")
                """
                In the following if statement we disable the default
                blocking behaviour by passing False for the blocking flag.
                """
                if container.acquire(False):
                    print("Consumed an item.")
                else:
                    print("Empty, skipping.")

        threads = []
        nloops = random.randrange(3, 6)

        print("Starting with %s items." % max_items)
        threads.append(Thread(target=producer, args=(nloops,)))
        threads.append( 
            Thread(
                target = consumer
                , args = (random.randrange(nloops, nloops+max_items+2),)
            )
        )
        for thread in threads: # Starts all the threads.
            thread.start()
        for thread in threads: # Waits for threads to complete before moving on with the main script.
            thread.join()

        print("All done.")

        pass

    @staticmethod
    def test002():
        import threading
        num = 0
        print('Before Lock acquire 001')
        # lock = threading.Lock()
        lock = threading.RLock()
        lock.acquire()
        num += 1
        print('Before Lock acquire 002')
        lock.acquire() # This will block.
        num += 2
        lock.release()
        pass

    @staticmethod
    def test001():
        from random import randrange
        from threading import Barrier, Thread
        from time import ctime, sleep
        num = 4
        # 4 threads will need to pass this barrier to get released.
        b = Barrier(num)
        names = ["Harsh", "Lokesh", "George", "Iqbal"]

        def player():
            name = names.pop()
            sleep(randrange(2, 5))
            print("%s reached the barrier at: %s" % (name, ctime()))
            b.wait()

        threads = []
        print("Race starts now…")
        for i in range(num):
            threads.append(Thread(target=player))
            threads[-1].start()
        """
        Following loop enables waiting for the threads to complete before
        moving on with the main script.
        """
        for thread in threads:
            thread.join()
        print()
        print("Race over!")
        pass

class Test_Basic(unittest.TestCase):

    def test_add(self):
        self.assertEqual(Tools_Basic.add(), 5)
    pass

    def test_multiply(self):
        self.assertEqual(Tools_Basic.multiply(), 0)
    pass

class Test_MongoDb(unittest.TestCase):
    
    def setUp(self):
        self.mongodb = MongoDb()
        self.mongodb.connection()
        pass

    def tearDown(self):
        pass

    def test_select(self):
        x = 0
        self.assertEqual(
            x, 0
        )
        pass

if __name__ == "__main__":
    unittest.main()




