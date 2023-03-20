
def delete_all_tmp_files():
    dir = 'files'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
