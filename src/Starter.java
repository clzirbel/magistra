//import java.awt.*;
import javax.swing.*;

class Starter {

	public static void main(String[] args)
	{
		Starter s = new Starter();
		s.run();
	}
	
	public void run()
	{
		String userChoice = 
			JOptionPane.showInputDialog("Welcome to Magistra!\n\n" + "What is your name?");
		String name = userChoice;
		
		userChoice = JOptionPane.showInputDialog("What language would you like to work on?");
		String language = userChoice;
		
		userChoice = JOptionPane.showInputDialog("What level would you like to start on? \nLevel 0 selects randomly from the whole list.\nLevel 1, 2, 3, starts with group 1, 2, 3, presenting the words you've gotten wrong.\nLevel -1, -2, -3 is the same, but omits the words you've gotten right twice in a row.");
		
		// System.out.println(name + language + level);
		
		Magistra m = new Magistra();
		m.run(language, name, userChoice, "", "");
	}
}
