import png


if __name__=="__main__":
    fname = "extracted_pngs/f3.png"
    f1 = png.Reader(fname)
    chunkiter = f1.chunks()
