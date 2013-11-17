// Practice.java
import java.awt.*;

import javax.swing.*;

public class Practice {
    public Practice (WordList WL) {

    JFrame frame = new JFrame("Magistra");
    Container pane = frame.getContentPane();
    
    int L = 0;  // default is to start with the base language
    int n = 0;  // first pair to practice

    WordPair WP;
    WP = WL.getSelectedPair(n);

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

    pane.setLayout(new GridLayout(6,2));
    

    JLabel baseLang    = new JLabel(WL.getLanguage(L));
    JLabel baseWord    = new JLabel(WP.getWord(L));
    JLabel foreignLang = new JLabel(WL.getLanguage(1-L));
    JTextField input   = new JTextField(40);
    JLabel status      = new JLabel("You know " + WL.getNumKnown() + " words.  Group " + WP.getGroup() + " " + WP.getUserData());
    JLabel help        = new JLabel("");
    JButton skip       = new JButton("Skip once");
    JButton forever    = new JButton("Skip forever");
    JButton switchDir  = new JButton("Switch direction");
    JButton exit       = new JButton("Save and exit");
    JLabel kb1;
    JLabel kb2;
    if (WL.getLanguage(1-L).equals("German"))
    {
    	kb1 = new JLabel("Press Alt-Left Shift for the German keyboard, then");
    	kb2 = new JLabel("y for z, z for y, ; for ö, ' for ä, [ for ü, - for ß, _ for ?, < for ;");
    }
    else if (WL.getLanguage(1-L).equals("Spanish"))
    {
    	kb1 = new JLabel("Press Alt-Left Shift for the Spanish keyboard, then");
    	kb2 = new JLabel("; for ñ, = for ¡, _ for ?, + for ¿, ' and a letter for é, í, ú, ó, á");
    }
    else 
    {
    	kb1 = new JLabel("");
    	kb2 = new JLabel("");
    }
//    pane.setLayout(new GridLayout(6,2));

    pane.add(baseLang);
    pane.add(baseWord);
//    foreignLang.setMinimumSize(new Dimension(100,100));
//    foreignLang.setPreferredSize(new Dimension(100,100));
    pane.add(foreignLang);
    pane.add(input);
    pane.add(status);
    pane.add(help);
    pane.add(skip);
    pane.add(switchDir);
    pane.add(forever);
    pane.add(exit);
    pane.add(kb1);
    pane.add(kb2);

    PracticeListener listener = new PracticeListener (WL, n, L, WP, baseLang, baseWord, foreignLang, input, status, help);

    input.addActionListener(listener);
    skip.addActionListener(listener);
    forever.addActionListener(listener);
    switchDir.addActionListener(listener);
    exit.addActionListener(listener);


    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.pack();
    frame.setVisible(true);
    
    }
}
