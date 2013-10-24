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
    int NumTries = 0;
    String pc = "";                    // portion correct, when wrong
    
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
		WP.modifyPairData("f");
		ReadyForNextPair = true;
    }
	else {
		 JTextField inputString = (JTextField)e.getSource();
		 if (CurrentPreview) 
		 {
			 ReadyForNextPair = true;                                // being previewed now, don't mark as correct
		 }
		 else if (WP.compareStrings(1-L, inputString.getText()))    // correct answer
		 {
			 if ((L==0) && (NumTries <= 1)) {                    // correct answer on first attempt
	           	 WL.changeNumKnown(UserData.evaluatePairData(WP.getUserData()+"+")-UserData.evaluatePairData(WP.getUserData()));
		    	 WP.modifyPairData("+");
		     }
		     else if (NumTries <= 1) {                           // correct answer, but translating the "easy" direction
		    	 WP.modifyPairData("#");
	         }
		     else {
		    	 WL.revisitLater(n,10);                          // correct answer on later attempt
		     }
			 ReadyForNextPair = true;
		 }
		 else if (inputString.getText().length() == 0) {
			 if (NumTries == 0) {
	    		 WL.changeNumKnown(UserData.evaluatePairData(WP.getUserData()+"-")-UserData.evaluatePairData(WP.getUserData()));
	             WP.modifyPairData("-");
			 }	 
			 NumTries = 1;                                       // 
			 pc = WP.getWord(1-L);                               // show correct answer
	         input.setText("");
	         help.setText(pc);
	         ReadyForNextPair = false;
		 }
	     else {                                                  // incorrect answer, but something
         pc = WP.getWord(1-L);
	     if (L==0) {                                             // "hard" direction
	    	 if (NumTries == 0) {
	    		 pc = WP.portionCorrect(1-L,inputString.getText());
	    	 }
	    	 else if (NumTries == 1) {
	    		 WL.changeNumKnown(UserData.evaluatePairData(WP.getUserData()+"-")-UserData.evaluatePairData(WP.getUserData()));
	             WP.modifyPairData("-");
	    	 }
	     }
	     else if (NumTries == 0) {
    		 pc = WP.portionCorrect(1-L,inputString.getText());
	     }
	     else if (NumTries == 1) {
    		 WP.modifyPairData("=");
	     }
	     
         input.setText("");
         help.setText(pc);
         ReadyForNextPair = false;
	     //          long startTime = System.currentTimeMillis();
         //          while (System.currentTimeMillis() < startTime + 1);
	     }
		 NumTries++;
	}

    if (ReadyForNextPair) {
	    n++;
	    NumTries = 0;
	    if (n >= WL.getNumToPractice()) {
	    	WL.writeUserData();
	        System.exit(0);
	    }
	    WP = WL.getSelectedPair(n);
        baseLang.setText(WL.getLanguage(L));
        baseWord.setText(WP.getWord(L));
        foreignLang.setText(WL.getLanguage(1-L));
        if (WP.getUserData().length() == 0) {
        	input.setText(WP.getWord(1-L));
        	help.setText("Preview: study it and hit Enter");
        	WP.modifyPairData("P");                               // previewed
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