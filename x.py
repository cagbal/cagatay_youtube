import time
import argparse


parser = argparse.ArgumentParser(description='Tek for loop')
parser.add_argument('--maksimum', type=int,
                   help='Kaca kadar sayalim?')

args = parser.parse_args()

baslangic_zaman = time.process_time()

counter = 0

for i in range(args.maksimum):
    counter += 1

bitis_zaman = time.process_time()

print("Harcanan zaman: {}".format(bitis_zaman-baslangic_zaman))
