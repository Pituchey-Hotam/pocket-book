from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import sys
import pdfbooklet_new
import pathlib
import math
def extract_num_of_pages(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()
    return number_of_pages

def split(path, name_of_split, sp, length, bind_method = 's'):
    #length += (4-(length%4))*(length%4 > 0)
    pdf = PdfFileReader(path)
    output = f'{name_of_split}'
    pdf_writer = PdfFileWriter()
    
    for page in range(sp,sp+length):
        if page<pdf.getNumPages():
            pdf_writer.addPage(pdf.getPage(page))
        else:
            pdf_writer.addBlankPage()
    if not bind_method == 's':
        pdf_writer.insertBlankPage(0)
        pdf_writer.addBlankPage()

    with open(output, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    output_pdf.close()

def split_Even_Odd(path, name_of_split):
    pdf = PdfFileReader(path)
    output_ev = f'{name_of_split}_even.pdf'
    output_odd = f'{name_of_split}_odd.pdf'
    pdf_writer_ev = PdfFileWriter()
    pdf_writer_odd = PdfFileWriter()
    number_of_pages=extract_num_of_pages(path)
    number_of_pages_plusblank= int((4-(number_of_pages/2 %4))*(number_of_pages/2 %4 > 0))
    for page in range(number_of_pages+number_of_pages_plusblank):
        if page<number_of_pages:
            if page % 2 == 0:
                pdf_writer_odd.addPage(pdf.getPage(page))
            else:
                pdf_writer_ev.addPage(pdf.getPage(page))
        else:
            pdf_writer_ev.addBlankPage()
            pdf_writer_odd.addBlankPage()
    
    with open(output_ev, 'wb') as output_pdf:
        pdf_writer_ev.write(output_pdf)
    output_pdf.close()
    with open(output_odd, 'wb') as output_pdf:
        pdf_writer_odd.write(output_pdf)
    output_pdf.close()

def rotate(path, name_of_rotate, num_rot=3):
    pdf = PdfFileReader(path)
    number_of_pages = extract_num_of_pages(path)
    output = f'{name_of_rotate}'
    pdf_writer = PdfFileWriter()
    for page in range(number_of_pages):
        page_1 = pdf.getPage(page).rotateClockwise(90*num_rot)
        pdf_writer.addPage(page_1)
    
    with open(output, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    output_pdf.close()       

def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

def merge_sort_pdfs(path1, path2, output):
    pdf_writer = PdfFileWriter()
    pdf1 = PdfFileReader(path1)
    pdf2 = PdfFileReader(path2)
    number_of_pages = extract_num_of_pages(path1)
    for page in range(number_of_pages):
        pdf_writer.addPage(pdf1.getPage(page))
        pdf_writer.addPage(pdf2.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)       

def pile_combine(file, path, file_name):
    tmp_num = extract_num_of_pages(file)
    split(file, path+file_name+'s1.pdf', 0, math.ceil(tmp_num/2))
    split(file, path+file_name+'s2.pdf', math.ceil(tmp_num/2), tmp_num)
            
    merge_sort_pdfs(path+file_name+'s1.pdf', path+file_name+'s2.pdf', file)


if __name__ == '__main__':
    #argv = sys.argv
    #argv=['', "C:\\Users\\user\\Downloads\\pdfbooklet-master\\", 'Feast', '8'] 
    old_path=input("Enter file location (example: C:\\Users\\user\\Downloads\\ ): ") #argv[1]
    file_name=input("Enter file name (example: my_book): ")#argv[2]
    path=old_path+'trash '+ file_name+'\\' #argv[2]+'\\'
    if not os.path.exists(path):
        os.mkdir(path)
    file = old_path+file_name+'.pdf' #argv[1]+argv[2]+'.pdf'
    notebook_len= int(input("Enter number of pages in each booklet (In multiples of 4. the standart is 32): "))#int(argv[3])
    pages_per_sheet = int(input("Enter pages per sheet (2/4/8): " ))#int(argv[4])
    bind_method = input("Sewing or gluing? In the gluing there is an extra blank page on each side. For the sewing enter 's' otherwise (if u r lazy) press 'Enter': ")#argv[5]
    combine_method = input("If u r doing only one notebook - enter 'v', otherwise press 'enter' (note: be specific...): ")#argv[6]
    #path=pathlib.Path(__file__).parent.resolve()
    number_of_pages = extract_num_of_pages(file)
    
    paths=[]
    if not bind_method == 's':
        notebook_len -=2
    for i in range(int(number_of_pages/notebook_len)+(number_of_pages%notebook_len > 0)):
        split(file, path+file_name+str(i+1)+'.pdf', i*notebook_len, notebook_len, bind_method)
        pdfbooklet_new.pdfbooklet( path+file_name+str(i+1)+'.pdf', path+file_name+str(i+1)+'let.pdf')
        paths.append(path+file_name+str(i+1)+'let.pdf')
    if pages_per_sheet == 2:
            path=old_path
    final_path = path+file_name+'_merged.pdf'
    merge_pdfs(paths, output=final_path)
    if pages_per_sheet>2:
        split_Even_Odd(final_path, path+file_name)
    
        
        rotate(path+file_name+'_odd.pdf', path+file_name+'_odd_rotated.pdf')
        rotate(path+file_name+'_even.pdf', path+file_name+'_even_rotated.pdf')
        
        if combine_method=='v':
            odd_path = path+file_name+'_odd_rotated.pdf'
            even_path = path+file_name+'_even_rotated.pdf'
            pile_combine(odd_path,path, file_name)
            pile_combine(even_path, path, file_name)
        
        odd_path = path+file_name+'_odd_let.pdf'
        even_path = path+file_name+'_even_let.pdf'
        pdfbooklet_new.pdfbooklet( path+file_name+'_odd_rotated.pdf', odd_path, 1, booklet= 0)
        pdfbooklet_new.pdfbooklet( path+file_name+'_even_rotated.pdf', even_path, 1, booklet= 0)

        if pages_per_sheet > 4:
            rotate(odd_path, path+file_name+'_odd_rotated2.pdf')
            rotate(even_path, path+file_name+'_even_rotated2.pdf',1)
            if combine_method=='v':
                odd_path = path+file_name+'_odd_rotated2.pdf'
                even_path = path+file_name+'_even_rotated2.pdf'
                pile_combine(odd_path,path, file_name)
                pile_combine(even_path, path, file_name)

            odd_path = path+file_name+'_odd_let2.pdf'
            even_path = path+file_name+'_even_let2.pdf'
            pdfbooklet_new.pdfbooklet( path+file_name+'_odd_rotated2.pdf', odd_path, booklet= 0)
            pdfbooklet_new.pdfbooklet( path+file_name+'_even_rotated2.pdf', even_path, booklet= 0, eng=1)

        final_path = old_path+file_name+' ready to print.pdf'
        merge_sort_pdfs(odd_path, even_path, final_path)
    
    print("Completed! Book is in "+final_path)