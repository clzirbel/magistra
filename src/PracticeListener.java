// PracticeListener.java

import javax.swing.*;
import java.awt.event.*;

class PracticeListener implements ActionListener {

    private WordList WL;
    private int n;
    private int L;
    private WordPair WP;
    private JLabel baseLang, baseWord, foreignLang, status, help;
    private JTextField input;
    boolean ReadyForNextPair = false;
    boolean CurrentPreview = false;
    
    PracticeListener ( WordList WL, int n, int L, WordPair WP, JLabel baseLang, JLabel baseWord, JLabel foreignLang, JTextField input, JLabel status, JLabel help) {
		this.WL = WL;
	    this.n = n;
	    this.L = L;
		this.WP = WP;
		this.baseLang = baseLang;
		this.baseWord = baseWord;
		this.foreignLang = foreignLang;
		this.input = input;
		this.status = status;
		this.help = help;
    }

    public void actionPerformed (ActionEvent e) {
	if (e.getActionCommand().equals("Switch direction")) {
	    L = 1 - L;
		ReadyForNextPair = true;
	}
	else if (e.getActionCommand().equals("Exit")) {
	    WL.writeUserData();
        System.exit(0);
	}
	else if (e.getActionCommand().equals("Skip once")) {
		ReadyForNextPair = true;
    }
	else if (e.getActionCommand().equals("Skip forever")) {
		WP.setFirstResult('f');
		ReadyForNextPair = true;
    }
	else {
		 JTextField inputString = (JTextField)e.getSource();
		 if (CurrentPreview) 
		 {
			 ReadyForNextPair = true;                                // being previewed now, don't mark as correct
		 }
		 else if (WP.compareStrings( 1-L, inputString.getText()))    // correct answer
		 {
			 if ((L==0) && (WP.getNumTries() == 0)) {                    // correct answer on first attempt
		    	 WP.setFirstResult('+');
	           	 WL.changeNumKnown(UserData.evaluatePairData(WP.getUserData()+"+")-UserData.evaluatePairData(WP.getUserData()));
		     }
		     else if (WP.getNumTries() == 0) {        // correct answer, but translating the "easy" direction
		    	 WP.setFirstResult('#');
	         }
		     else {
		    	 WL.revisitLater(n,10);
		     }
			 ReadyForNextPair = true;
		 }
	     else {                                  // incorrect answer
	     if (L==0) {
               WP.setFirstResult('-');
               WL.changeNumKnown(UserData.evaluatePairData(WP.getUserData()+"-")-UserData.evaluatePairData(WP.getUserData()));
               ReadyForNextPair = false;
	     }
	     else WP.setFirstResult('=');
	      WP.registerTry();
          input.setText("");
          help.setText(WP.getWord(1-L));
          ReadyForNextPair = false;
	  //          long startTime = System.currentTimeMillis();
	  //          while (System.currentTimeMillis() < startTime + 1);
	}
	}

    if (ReadyForNextPair) {
	    n++;
	    if (n >= WL.getNumToPractice()) {
	    	WL.writeUserData();
	        System.exit(0);
	    }
	    WP = WL.getSelectedPair(n);
        baseLang.setText(WL.getLanguage(L));
        baseWord.setText(WP.getWord(L));
        foreignLang.setText(WL.getLanguage(1-L));
        if (WP.getUserData().length() == 0 & WP.getFirstResult() == '?') {
        	input.setText(WP.getWord(1-L));
        	help.setText("Preview; study it and hit Enter");
        	WP.setFirstResult('P');                               // previewed
        	WL.revisitLater(n, 5);                                // queue up to revisit later
        	CurrentPreview = true;
        }
        else {
            input.setText("");
            help.setText("");
            CurrentPreview = false;
        }
        status.setText("You know " + WL.getNumKnown() + " words.  Group " + WP.getGroup() + " " + WP.getUserData());
    }
    }
}