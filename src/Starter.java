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

		userChoice = JOptionPane.showInputDialog("What level would you like to start on?");
		String level = userChoice;

		userChoice = JOptionPane.showInputDialog("What percentage of known words to practice?");
		String percentage = userChoice;

		// System.out.println(name + language + level);

		Magistra m = new Magistra();
		m.run(language, name, level, percentage, "", "");
	}
}
