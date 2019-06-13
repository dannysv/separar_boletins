import org.apache.pdfbox.multipdf.Splitter;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.PDPageContentStream;
import org.apache.pdfbox.pdmodel.font.PDType1Font;

import java.io.File;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.util.List;
import java.util.Iterator;
import java.io.PrintWriter;
import java.util.ArrayList;

public class edit_pdf{
	public static void main(String[] args) throws IOException{
		
		String path1 = "../data/Boletins/Boletins1";
		String path_out1 = "../temp/Boletins/Boletins1";
		edit_pdf_folder(path1, path_out1);

		String path2 = "../data/Boletins/Boletins2";
		String path_out2 = "../temp/Boletins/Boletins2";
		edit_pdf_folder(path2, path_out2);

		String path3 = "../data/Boletins/Boletins3";
		String path_out3 = "../temp/Boletins/Boletins3";
		edit_pdf_folder(path3, path_out3);
		

		String path4 = "../data/Boletins/Boletins4";
		String path_out4 = "../temp/Boletins/Boletins4";
		edit_pdf_folder(path4, path_out4);

	}

   	public static String[] list_files(String str_folder)
    	{
		File folder = new File(str_folder);
		String[] files = folder.list();
		return files;
    	}

   	public static void edit_pdf_folder(String path, String path_out) throws FileNotFoundException, IOException{
		String[] l_files = list_files(path);
        	for (String fle: l_files){
			String filein = path + "/" + fle;
			String fileout = path_out + "/" + fle+"_edit.pdf";
            		edit_pdf_file(filein, fileout);
        	}
   	}


	public static void edit_pdf_file(String filename, String out) throws IOException{
		File file = new File(filename);
		PDDocument document = PDDocument.load(file);
		Splitter splitter = new Splitter();
		List<PDDocument> Pages = splitter.split(document);
		Iterator<PDDocument> iterator = Pages.listIterator();
		ArrayList pages_t = new ArrayList();
		int i = 0;
		while(iterator.hasNext()) {
			PDDocument pd = iterator.next();
			PDPage page = pd.getPage(0);
			pages_t.add(page);

			PDPage senial = new PDPage();
			PDPageContentStream contentStream = new PDPageContentStream(document, senial, PDPageContentStream.AppendMode.APPEND,true,true);
			contentStream.beginText();
			contentStream.setFont(PDType1Font.TIMES_ROMAN, 18);
			contentStream.newLineAtOffset(100, 10);
			String text = "### new line ###";
			contentStream.showText(text);
			contentStream.endText();
			//System.out.println("Content added");
			contentStream.close();
			pages_t.add(senial);
		}
		//document.close();
		System.out.println("Ok");
		int num_pages = pages_t.size();
		System.out.println(num_pages);
		PDDocument document_d = new PDDocument();
		for (int k=0;k<num_pages;k++){
			document_d.addPage((PDPage)pages_t.get(k));
		}

		document_d.save(out);
		document_d.close();
		document.close();
		//document_d.close();
	}

}
