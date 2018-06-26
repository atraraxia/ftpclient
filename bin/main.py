
import bin.ftp

if __name__ == '__main__':
    bin.ftp.buildftp = bin.ftp.BuildFtp(bin.ftp.root)
    bin.ftp.root.mainloop()
