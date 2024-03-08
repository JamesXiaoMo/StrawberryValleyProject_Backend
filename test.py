if __name__ == '__main__':
    with open('data_table.json', 'rb') as f:
        print(len(f.read())/1024)