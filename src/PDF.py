import tabula

class PDFExtract:
 
    def read_pdf(pdffile, pdfpass, area_table=[], pdfpages='all', ignore_header=False, pdfcolumns=[], streammode=False):
        if ignore_header:
            pd_option = ({'header': None} )
        else: 
            pd_option = {}
        return tabula.read_pdf(pdffile, 
                               password=pdfpass, 
                               pages=pdfpages, 
                               area=area_table, 
                               pandas_options=pd_option, 
                               columns=pdfcolumns,
                               relative_columns=True, 
                               stream=streammode,
                               )
        