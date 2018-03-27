from PyPDF2 import PdfFileMerger



class Tools_PDF:
    # https://stackoverflow.com/questions/3444645/merge-pdf-files
    @staticmethod
    def merge_pdf(
        merged_pdf = "result.pdf"

        , list_pdf = [
            r'C:\Program Files (x86)\Foxit Software\Foxit Reader\stamps\Standard Templates\Ellipse Stamp(Purple).pdf'
            , r'C:\Program Files (x86)\Foxit Software\Foxit Reader\stamps\Standard Templates\Triangle Stamp(Blue).pdf'
            , r'C:\Program Files (x86)\Foxit Software\Foxit Reader\stamps\Standard Templates\Triangle Stamp(Purple).pdf'
        ]
    ):
        merger = PdfFileMerger()

        for pdf in list_pdf:
            merger.append(pdf)

        merger.write(merged_pdf)
        print()
        print("Merge Complete")
        pass