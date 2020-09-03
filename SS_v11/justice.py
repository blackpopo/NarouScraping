def justice(n):
    if n==1:
        return 2
    else:
        survivor = justice(n-1)
        print('{} peoples are killed in {} peaples'.format(survivor-1, survivor*2-1))
        return survivor*2-1

if __name__=='__main__':
    justice(100)