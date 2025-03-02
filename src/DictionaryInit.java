// DictionaryInit.java
import java.awt.*;
import javax.swing.Box;
import javax.swing.JFrame;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

public class DictionaryInit {
    public DictionaryInit (WordList WL) {
	
    JFrame frame = new JFrame("Magistra editor");

    frame.setLayout(new FlowLayout());
    
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

    int fontSize = 16;
    int fieldWidth = fontSize*24;
    int fieldHeight = fontSize*2;
    Font textFont = new Font("SansSerif", Font.PLAIN, fontSize);

    Label baseLang          = new Label(WL.getLanguage(0)+" (hit Enter to add pair)");
    TextField baseWord      = new TextField(30);
    Label foreignLang       = new Label(WL.getLanguage(1));
    TextField foreignWord   = new TextField(30);
    Label groupLabel        = new Label("Group (hit enter to add pair) -->");
    TextField group         = new TextField("20");
    TextArea baseDisplay    = new TextArea(20,30);
    TextArea foreignDisplay = new TextArea(20,30);
    Label editentrylabel    = new Label("Edit this entry -->");
    TextField editentry     = new TextField("");
    Label changegrouplabel  = new Label("Change group of this entry to current group -->");
    TextField changegroup   = new TextField("");
    Label removelabel       = new Label("Remove this entry -->");
    TextField remove        = new TextField("");
    Button exit             = new Button("Save and Exit");
    Button clear            = new Button("Clear");
    Label kb1;

    baseLang.setFont(textFont);
    baseWord.setFont(textFont);
    foreignLang.setFont(textFont);
    foreignWord.setFont(textFont);
    groupLabel.setFont(textFont);
    group.setFont(textFont);
    baseDisplay.setFont(textFont);
    foreignDisplay.setFont(textFont);
    editentrylabel.setFont(textFont);
    editentry.setFont(textFont);
    changegrouplabel.setFont(textFont);
    changegroup.setFont(textFont);
    removelabel.setFont(textFont);
    remove.setFont(textFont);
    exit.setFont(textFont);
    clear.setFont(textFont);


    int maxnumfound = 20;
    int[] foundarray = new int[maxnumfound];
    
    int beingedited = -1;    // -1 means that the word pair is new

    if (WL.getLanguage(1).equals("German"))
    {
    	kb1 = new Label("Press Alt-Left Shift for the German keyboard, then y for z, z for y, ; for ö, ' for ä, [ for ü, - for ß, _ for ?, < for ;");
    }
    else if (WL.getLanguage(1).equals("Spanish"))
    {
    	kb1 = new Label("Press Alt-Left Shift for the Spanish keyboard, then ; for ñ, = for ¡, _ for ?, + for ¿, ' and a letter for é, í, ú, ó, á");
    }
    else 
    {
    	kb1 = new Label("");
    }

    kb1.setFont(textFont);

    Dimension D = new Dimension(300,24);
    foreignLang.setPreferredSize(D);
    baseLang.setPreferredSize(D);
    groupLabel.setPreferredSize(D);
    group.setPreferredSize(D);
    group.setMinimumSize(D);                   // can't get this box to be the right size when it has text in it!
    editentrylabel.setPreferredSize(D);
    editentry.setPreferredSize(D);
    changegrouplabel.setPreferredSize(D);
    changegroup.setPreferredSize(D);
    removelabel.setPreferredSize(D);
    remove.setPreferredSize(D);
    exit.setPreferredSize(D);
    clear.setPreferredSize(D);
    kb1.setPreferredSize(new Dimension(600,24));

    Container row1 = Box.createHorizontalBox();
    Container row2 = Box.createHorizontalBox();
    Container row3 = Box.createHorizontalBox();
    Container row4 = Box.createHorizontalBox();
    Container row5 = Box.createHorizontalBox();
    Container row6 = Box.createHorizontalBox();
    Container row7 = Box.createHorizontalBox();
    Container row8 = Box.createHorizontalBox();
    Container row9 = Box.createHorizontalBox();

    row1.add(foreignLang);
    row1.add(baseLang);
    row2.add(foreignWord);
    row2.add(baseWord);
    row3.add(groupLabel);
//    row3.add(Box.createHorizontalGlue());
    row3.add(group);
    row4.add(foreignDisplay);
    row4.add(baseDisplay);
    row5.add(editentrylabel);
    row5.add(editentry);
    row6.add(changegrouplabel);
    row6.add(changegroup);
    row7.add(removelabel);
    row7.add(remove);
    row8.add(exit);
    row8.add(clear);
    row9.add(kb1);

    Container allRows = Box.createVerticalBox();
    
    allRows.add(row1);
    allRows.add(row2);
    allRows.add(row3);
    allRows.add(row4);
    allRows.add(row5);
    allRows.add(row6);
    allRows.add(row7);
    allRows.add(row8);
    allRows.add(row9);
    frame.add(allRows);

    DictionaryListener listener = new DictionaryListener (WL, baseWord, foreignWord, baseDisplay, foreignDisplay, foundarray, beingedited);
    DictionaryActionListener actionlistener = new DictionaryActionListener(WL, baseWord, foreignWord, group, baseDisplay, foreignDisplay, editentry, changegroup, remove, foundarray, beingedited, frame);

    baseWord.addTextListener(listener);
    foreignWord.addTextListener(listener);
    baseWord.addActionListener(actionlistener);
    foreignWord.addActionListener(actionlistener);
    exit.addActionListener(actionlistener);
    clear.addActionListener(actionlistener);
    group.addActionListener(actionlistener);
    changegroup.addActionListener(actionlistener);
    editentry.addActionListener(actionlistener);
    remove.addActionListener(actionlistener);

    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setVisible(true);
    frame.pack();
    }
}
