
// package ui;

import java.awt.Component;
import java.awt.Dimension;
import java.awt.DisplayMode;
import java.awt.Font;
import java.awt.GraphicsEnvironment;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.NoSuchElementException;
import java.util.StringTokenizer;

import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

/**
 * Represents the window launched to start Magistra.
 * 
 * @author Dominic
 */
public class Launcher extends JFrame implements ActionListener
{
	private JButton practiceButton;
	private JButton dictionaryButton;
	private TextBox nameField;
	private TextBox languageField;
	private TextBox levelField;
	private TextBox dictionaryPathField;
	private TextBox userDataPathField;
	
	private static final long serialVersionUID = 1L;
	
	private static final String nameDescription = "Name";
	private static final String languageDescription = "Language";
	private static final String levelDescription = "Level";
	private static final String dictionaryPathDescription = "Dictionary Path";
	private static final String userDataPathDescription = "User Data Path";
	private static final String practiceButtonDescription = "Practice words";
	private static final String dictionaryButtonDescription = "Edit word list";
	
	/**
	 * Invoked to run the Launcher.
	 * 
	 * @param args - the command-line arguments (ignored)
	 */
	public static void main(String[] args)
	{
		new Launcher();
	}
	
	/**
	 * Creates a new Launcher with the default name, "Magistra Launcher".
	 */
	public Launcher()
	{
		this("Magistra Launcher");
	}
	
	/**
	 * Creates a new Launcher with the given name, used to name the Window.
	 * 
	 * @param name - the name of the Launcher window
	 */
	public Launcher(String name)
	{
		super(name);
		
		// set the look-and-feel
		String laf = UIManager.getSystemLookAndFeelClassName();
		try
		{
			UIManager.setLookAndFeel(laf);
		}
		catch (UnsupportedLookAndFeelException exc)
		{
			System.err.println ("[WARNING] Unsupported Look and Feel: " + laf + ".");
		}
		catch (Exception exc)
		{
			System.err.println ("[WARNING] Error loading " + laf + ": " + exc + ".");
		}
		
		// create and size the components
		
		nameField = new TextBox(nameDescription);
		languageField = new TextBox(languageDescription);
		levelField = new TextBox(levelDescription);
		dictionaryPathField = new TextBox(dictionaryPathDescription);
		userDataPathField = new TextBox(userDataPathDescription);
		practiceButton = new JButton(practiceButtonDescription);
		dictionaryButton = new JButton(dictionaryButtonDescription);
		
		int fontSize = 16;
		int fieldWidth = fontSize*24;
		int fieldHeight = fontSize*2;
		int buttonWidth = fontSize*10;
		int buttonHeight = fontSize*3;

		Font textFont = new Font("SansSerif", Font.PLAIN, fontSize);

		nameField.setMinimumSize(new Dimension(fieldWidth, fieldHeight));
		languageField.setMinimumSize(new Dimension(fieldWidth, fieldHeight));
		levelField.setMinimumSize(new Dimension(fieldWidth, fieldHeight));
		dictionaryPathField.setMinimumSize(new Dimension(fieldWidth, fieldHeight));
		userDataPathField.setMinimumSize(new Dimension(fieldWidth, fieldHeight));
		practiceButton.setMinimumSize(new Dimension(buttonWidth, buttonHeight));
		dictionaryButton.setMinimumSize(new Dimension(buttonWidth, buttonHeight));
		
		nameField.setMaximumSize(new Dimension(fieldWidth, fieldHeight));
		languageField.setMaximumSize(new Dimension(fieldWidth, fieldHeight));
		levelField.setMaximumSize(new Dimension(fieldWidth, fieldHeight));
		dictionaryPathField.setMaximumSize(new Dimension(fieldWidth, fieldHeight));
		userDataPathField.setMaximumSize(new Dimension(fieldWidth, fieldHeight));
		practiceButton.setMaximumSize(new Dimension(buttonWidth, buttonHeight));
		dictionaryButton.setMaximumSize(new Dimension(buttonWidth, buttonHeight));
		
		nameField.setFont(textFont);
		languageField.setFont(textFont);
		levelField.setFont(textFont);
		dictionaryPathField.setFont(textFont);
		userDataPathField.setFont(textFont);
		practiceButton.setFont(textFont);
		dictionaryButton.setFont(textFont);

		practiceButton.addActionListener(this);
		dictionaryButton.addActionListener(this);
		
		// set the contents and tooltips of the components
		try
		{
			loadConfig();
		}
		catch (IOException ex) { }
		
		nameField.setToolTipText(nameDescription);
		languageField.setToolTipText(languageDescription);
		levelField.setToolTipText(levelDescription);
		dictionaryPathField.setToolTipText(dictionaryPathDescription);
		userDataPathField.setToolTipText(userDataPathDescription);

		
		// set the layout and add the components
		JPanel panel = new JPanel();
		JPanel buttonPanel = new JPanel();
		BoxLayout layout = new BoxLayout(panel, BoxLayout.PAGE_AXIS);
		GridLayout buttonLayout = new GridLayout();
		
		panel.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));
		panel.setLayout(layout);
		buttonPanel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));
		buttonPanel.setLayout(buttonLayout);
		
		buttonPanel.add(dictionaryButton);
		buttonPanel.add(practiceButton);
		
		panel.add(nameField, Component.CENTER_ALIGNMENT);
		panel.add(Box.createRigidArea(new Dimension(0, 10)));
		panel.add(languageField, Component.CENTER_ALIGNMENT);
		panel.add(Box.createRigidArea(new Dimension(0, 10)));
		panel.add(levelField, Component.CENTER_ALIGNMENT);
		panel.add(Box.createRigidArea(new Dimension(0, 10)));
		panel.add(dictionaryPathField, Component.CENTER_ALIGNMENT);
		panel.add(Box.createRigidArea(new Dimension(0, 10)));
		panel.add(userDataPathField, Component.CENTER_ALIGNMENT);
		panel.add(Box.createRigidArea(new Dimension(0, 10)));
		panel.add(buttonPanel, Component.CENTER_ALIGNMENT);
		
		// create the window
		getContentPane().add(panel);
		
		this.setResizable(true);
		DisplayMode mode = GraphicsEnvironment.getLocalGraphicsEnvironment().getDefaultScreenDevice().getDisplayMode();
		this.setMinimumSize(new Dimension(fieldWidth+20, fieldHeight*10+20));
		this.setLocation(mode.getWidth()/2 - getWidth()/2, mode.getHeight()/2 - getHeight()/2);
		this.setLocation(0,0);

	    this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		this.setVisible(true);
	}
	
	/**
	 * Invoked when an action is taken one of the buttons in the Launcher.
	 */
	public void actionPerformed(ActionEvent e)
	{
		if (e.getSource().equals(practiceButton))
		{
			try
			{
				saveConfig();
			}
			catch (IOException ex)
			{
				System.err.println("[WARNING] Error saving config.txt: " + ex.getMessage());
			}
			
			// launch magistra here to practice words
			
			Magistra m = new Magistra();
	    	m.run(nameField.getCurrentText(), languageField.getCurrentText(), levelField.getCurrentText(), dictionaryPathField.getCurrentText(), userDataPathField.getCurrentText()
);
			
			this.setVisible(false);
		}
		else if (e.getSource().equals(dictionaryButton))
		{
			try
			{
				saveConfig();
			}
			catch (IOException ex)
			{
				System.err.println("[WARNING] Error saving config.txt: " + ex.getMessage());
			}
			
			// launch the dictionary editor here.

			Dictionary d = new Dictionary();
			d.run(languageField.getCurrentText(),dictionaryPathField.getCurrentText());
			this.setVisible(false);
		}
	}
	
	/**
	 * Loads the config.txt file directly into the components of the Launcher by setting their current text.
	 * 
	 * @throws IOException - thrown if the file could not be read or there was an I/O error
	 */
	private void loadConfig() throws IOException
	{
		BufferedReader in = new BufferedReader(new FileReader("config.txt"));
		
		String line;
		while ((line = in.readLine()) != null)
		{
			if (line.trim().startsWith("#"))
			{
				continue;
			}
			
			String attribute;
			String value;
			try
			{
				StringTokenizer tokenizer = new StringTokenizer(line, ":");
				attribute = tokenizer.nextToken().trim();
				value = tokenizer.nextToken();
				while (tokenizer.hasMoreTokens())
				{
					value += ":" + tokenizer.nextToken();
				}
				value = value.trim();
			}
			catch (NoSuchElementException ex)
			{
				continue;
			}
			
			
			if (attribute.equalsIgnoreCase("name"))
			{
				nameField.setCurrentText(value);
			}
			else if (attribute.equalsIgnoreCase("language"))
			{
				languageField.setCurrentText(value);
			}
			else if (attribute.equalsIgnoreCase("level"))
			{
				levelField.setCurrentText(value);
			}
			else if (attribute.equalsIgnoreCase("dictionaryPath"))
			{
				dictionaryPathField.setCurrentText(value);
			}
			else if (attribute.equalsIgnoreCase("userDataPath"))
			{
				userDataPathField.setCurrentText(value);
			}
		}
		
		in.close();
	}
	
	/**
	 * Saves the config.txt file by writing the contents of the text boxes into the file.
	 * 
	 * @throws IOException - thrown if the file could not be read or there was an I/O error reading the file
	 */
	private void saveConfig() throws IOException
	{
		BufferedWriter out = new BufferedWriter(new FileWriter("config.txt"));
		
		out.write("name:" + nameField.getCurrentText());
		out.newLine();
		out.write("language:" + languageField.getCurrentText());
		out.newLine();
		out.write("level:" + levelField.getCurrentText());
		out.newLine();
		out.write("dictionaryPath:" + dictionaryPathField.getCurrentText());
		out.newLine();
		out.write("userDataPath:" + userDataPathField.getCurrentText());
		
		out.close();
	}
}
