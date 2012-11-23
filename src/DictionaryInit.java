// DictionaryInit.java
import java.awt.*;
// import javax.swing.*;
// import java.awt.event.*;

import javax.swing.JLabel;

public class DictionaryInit extends Frame {
    public DictionaryInit (WordList WL) {

	int L = 0;                         // which language to show first
	
    Panel p = new Panel();
    p.setLayout(new GridLayout(6,2));

    Label baseLang          = new Label(WL.getLanguage(0));
    TextField baseWord      = new TextField(30);
    Label foreignLang       = new Label(WL.getLanguage(1));
    TextField foreignWord   = new TextField(30);
    Button exit             = new Button("Exit");
    Label groupLabel        = new Label("Group");
    Button clear            = new Button("Clear");
    TextField group         = new TextField("25");
    TextArea baseDisplay    = new TextArea(4,30);
    TextArea foreignDisplay = new TextArea(4,30);
    TextField remove        = new TextField(30);
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

//    Label kb1         = new Label("Press Alt-Left Shift for the German keyboard, then");
//    Label kb2         = new Label("y for z, z for y, ; for ö, ' for ä, [ for ü, - for ß, _ for ?, < for ;"); 

    //    p.setLayout(new GridLayout(5,2));

    p.add(baseLang);
    p.add(foreignLang);
    p.add(baseWord);
    p.add(foreignWord);
    p.add(groupLabel);
    p.add(group);
    p.add(baseDisplay);
    p.add(foreignDisplay);
    p.add(exit);
    p.add(clear);
    p.add(kb1);
    p.add(kb2);

    add(p,"Center");

    remove.setText("No");
    
    DictionaryListener listener = new DictionaryListener (WL, baseWord, foreignWord, group, baseDisplay, foreignDisplay, L, remove);

    DictionaryActionListener actionlistener = new DictionaryActionListener(WL, baseWord, foreignWord, group, baseDisplay, foreignDisplay, L, remove);

    baseWord.addTextListener(listener);
    foreignWord.addTextListener(listener);
    remove.addActionListener(actionlistener);
    baseWord.addActionListener(actionlistener);
    foreignWord.addActionListener(actionlistener);
    exit.addActionListener(actionlistener);
    clear.addActionListener(actionlistener);
    group.addActionListener(actionlistener);

    setSize(600,500);
    setVisible(true);
    }
}
