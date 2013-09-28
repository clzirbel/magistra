// DictionaryInit.java
import java.awt.*;

import javax.swing.JFrame;
import javax.swing.JLabel;

public class DictionaryInit extends JFrame {
    public DictionaryInit (WordList WL) {
	
    Panel p = new Panel();
    p.setLayout(new GridLayout(9,2));

    Label baseLang          = new Label(WL.getLanguage(0)+" (hit Enter to add pair)");
    TextField baseWord      = new TextField(30);
    Label foreignLang       = new Label(WL.getLanguage(1));
    TextField foreignWord   = new TextField(30);
    Button exit             = new Button("Save and Exit");
    Label groupLabel        = new Label("Group (hit enter to add pair) -->");
    Button clear            = new Button("Clear");
    TextField group         = new TextField("25");
    TextArea baseDisplay    = new TextArea(4,30);
    TextArea foreignDisplay = new TextArea(4,30);
    Label editentrylabel    = new Label("Edit this entry -->");
    TextField editentry     = new TextField(30);
    Label changegrouplabel  = new Label("Change group of this entry to current group -->");
    TextField changegroup   = new TextField(30);
    Label removelabel       = new Label("Remove this entry -->");
    TextField remove        = new TextField(30);
    JLabel kb1;
    JLabel kb2;

    int maxnumfound = 20;
    int[] foundarray = new int[maxnumfound];
    
    int beingedited = -1;    // -1 means that the word pair is new

    if (WL.getLanguage(1).equals("German"))
    {
    	kb1 = new JLabel("Press Alt-Left Shift for the German keyboard, then");
    	kb2 = new JLabel("y for z, z for y, ; for ö, ' for ä, [ for ü, - for ß, _ for ?, < for ;");
    }
    else if (WL.getLanguage(1).equals("Spanish"))
    {
    	kb1 = new JLabel("Press Alt-Left Shift for the Spanish keyboard, then");
    	kb2 = new JLabel("; for ñ, = for ¡, _ for ?, + for ¿, ' and a letter for é, í, ú, ó, á");
    }
    else 
    {
    	kb1 = new JLabel("");
    	kb2 = new JLabel("");
    }

//    Label kb1         = new Label("Press Alt-Left Shift for the German keyboard, then");
//    Label kb2         = new Label("y for z, z for y, ; for ö, ' for ä, [ for ü, - for ß, _ for ?, < for ;"); 

    //    p.setLayout(new GridLayout(5,2));

    p.add(foreignLang);
    p.add(baseLang);
    p.add(foreignWord);
    p.add(baseWord);
    p.add(groupLabel);
    p.add(group);
    p.add(foreignDisplay);
    p.add(baseDisplay);
    p.add(editentrylabel);
    p.add(editentry);
    p.add(changegrouplabel);
    p.add(changegroup);
    p.add(removelabel);
    p.add(remove);
    p.add(exit);
    p.add(clear);
    p.add(kb1);
    p.add(kb2);

    add(p,"Center");
    
    DictionaryListener listener = new DictionaryListener (WL, baseWord, foreignWord, baseDisplay, foreignDisplay, foundarray, beingedited);

    DictionaryActionListener actionlistener = new DictionaryActionListener(WL, baseWord, foreignWord, group, baseDisplay, foreignDisplay, editentry, changegroup, remove, foundarray, beingedited);

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

    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    
    setSize(600,500);
    setVisible(true);
    }
}
