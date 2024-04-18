#!/usr/bin/env python3

from mysqlDB import addTo_tmpCart
from functions import fetch_products
from argparse import ArgumentParser
import sys

def dump():
    parser = ArgumentParser(description="Dump products to tmpCart")
    parser.add_argument("-n", "--num", help="Number of products to dump", type=int, required=True)
    args = parser.parse_args()

    if args.num <= 0:
        print("Number of products to dump must be greater than zero.")
        sys.exit(1)

    products = fetch_products(args.num)

    if not products:
        print("No products fetched to dump.")
        sys.exit(1)

    for product in products:
        addTo_tmpCart(product, 1)  # Assuming '1' is a placeholder user ID or similar identifier
    
    print(f"Dumped {args.num} products to tmpCart")

dump()