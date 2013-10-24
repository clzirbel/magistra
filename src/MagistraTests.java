

public class MagistraTests 
{
	public static void main(String[] args)
	{
		WordPair WP = new WordPair("nothing here","translation; tramp",3); 
	
		System.out.println(WP.portionCorrect(0, "trampoline"));		
		System.out.println(WP.portionCorrect(1, "trampoline"));		

	}
	
}
