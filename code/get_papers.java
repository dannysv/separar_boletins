import org.apache.pdfbox.multipdf.Splitter;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.PDPageContentStream;
import org.apache.pdfbox.pdmodel.font.PDType1Font;

import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.util.List;
import java.util.Iterator;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class get_papers{
	public static void main(String[] args)throws IOException{
		String path_pdf1 = "../data/Boletins/Boletins1/";
		String path_out1 = "../papers/Boletins/Boletins1/";
		String path_starts1 = "../indexs/Boletins/Boletins1/";
		get_papers_folder(path_pdf1, path_out1, path_starts1);
		
		String path_pdf2 = "../data/Boletins/Boletins2/";
		String path_out2 = "../papers/Boletins/Boletins2/";
		String path_starts2 = "../indexs/Boletins/Boletins2/";
		get_papers_folder(path_pdf2, path_out2, path_starts2);
		
		String path_pdf3 = "../data/Boletins/Boletins3/";
		String path_out3 = "../papers/Boletins/Boletins3/";
		String path_starts3 = "../indexs/Boletins/Boletins3/";
		get_papers_folder(path_pdf3, path_out3, path_starts3);
		
		String path_pdf4 = "../data/Boletins/Boletins4/";
		String path_out4 = "../papers/Boletins/Boletins4/";
		String path_starts4 = "../indexs/Boletins/Boletins4/";
		get_papers_folder(path_pdf4, path_out4, path_starts4);
	}

	public static String[] list_files(String str_folder)
        {
                File folder = new File(str_folder);
                String[] files = folder.list();
                return files;
        }


	public static void get_papers_folder(String path, String path_out, String path_starts) throws FileNotFoundException, IOException{
                String[] l_files = list_files(path);
                for (String fle: l_files){
			get_papers_file(path, fle, path_out, path_starts);
                }
        }



	public static void get_papers_file(String path_pdf, String filename, String path_out, String path_starts)throws IOException{
		//String path_starts = "./starts.txt";
		//String path_pdf = "./test.pdf";
		File file_starts = new File(path_starts+filename+"_edit.pdf.txt");
		BufferedReader br = new BufferedReader(new FileReader(file_starts));
		String starts="";
		String st="";
		while((st =br.readLine()) != null)
			starts = st;
		String[] l_starts = starts.split(",");
		
		String[] indexs= l_starts;
		List<String> l_indexs = Arrays.asList(indexs); 

		File f = new File(path_pdf+filename);
		PDDocument document = PDDocument.load(f);
		Splitter splitter = new Splitter();
		List<PDDocument> Pages = splitter.split(document);
		Iterator<PDDocument> iterator = Pages.listIterator();
		int i = 0;
		int cont_paper = 1;
		ArrayList pages = new ArrayList();
		while(iterator.hasNext()) {
			PDDocument pd = iterator.next();
			i+=1;
			//System.out.println("data type : " + l_indexs.get(0).getClass().getName());
			if( !Integer.toString(i).equals(l_indexs.get(0)) & l_indexs.contains(Integer.toString(i)))
			{
				System.out.println(Integer.toString(i) +"  :  " + l_indexs.get(0));
				//save the paper and increase the cont_paper
				System.out.println("aqui : "+Integer.toString(i));
				int num_pages = pages.size();
				System.out.println(num_pages);
				PDDocument document_d = new PDDocument();
				for (int k=0;k<num_pages;k++){
					document_d.addPage((PDPage)pages.get(k));
				}
				String out = path_out+filename+ "_paper_"+Integer.toString(cont_paper) + ".pdf";	
				document_d.save(out);
				document_d.close();
				//iniciar nuevamente
				System.out.println("aqui cerrar un paper y comenzar otro");
				pages = new ArrayList();
				cont_paper +=1;
			}
			if (i >= Integer.parseInt(l_indexs.get(0)))
			//if (cont_paper > 1)
			{
				PDPage p = pd.getPage(0);
				pages.add(p);
			}
			else{
				System.out.println(Integer.toString(i) + " ------ " + l_indexs.get(0) + " --- no será agregado" );
			}
		}

		//save the paper and increase the cont_paper
		System.out.println("aqui el último : "+Integer.toString(i));
		int num_pages = pages.size();
		System.out.println(num_pages);
		PDDocument document_d = new PDDocument();
		for (int k=0;k<num_pages;k++){
			document_d.addPage((PDPage)pages.get(k));
		}
		String out = path_out+filename+"_paper_"+Integer.toString(cont_paper) + ".pdf";	
		document_d.save(out);
		document_d.close();
		
		//cerrar el documento principal
		document.close();
	}
}
