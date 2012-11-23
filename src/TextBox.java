// package ui;

import java.awt.Color;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

import javax.swing.JTextField;

/**
 * Represents a TextBox with default text displayed in gray when the text box is empty and does not have focus.
 * 
 * @author Dominic
 */
public class TextBox extends JTextField implements FocusListener, KeyListener
{
	private boolean hasFocus;
	
	private static final long serialVersionUID = 1L;
	
	private String defaultText;
	private String currentText;
	
	/**
	 * Creates a new TextBox with the given default text.
	 * This text is displayed in gray when the text box is empty and does not have focus.
	 * By default the text that is actually in the box (the "current text") is empty.
	 * 
	 * @param defaultText - the text to be displayed by default
	 */
	public TextBox(String defaultText)
	{
		super();
		hasFocus = false;
		this.addFocusListener(this);
		this.addKeyListener(this);
		this.defaultText = defaultText;
		currentText = new String();
		
		setText(currentText);
	}
	
	/**
	 * Gets the text that is displayed by default when the text box is empty and does not have focus.
	 * 
	 * @return defaultText - the default text for this TextBox
	 */
	public String getDefaultText()
	{
		return defaultText;
	}
	
	/**
	 * Sets the text that is displayed by the default when the text is empty and does not have focus.
	 * 
	 * @param defaultText - the default text for this TextBox
	 */
	public void setDefaultText(String defaultText)
	{
		this.defaultText = defaultText;
	}
	
	/**
	 * Gets the text that is currently held by this text box.
	 * If the text box is empty and does not have focus, this method
	 *  will return an empty String rather than the default text.
	 * 
	 * @return currentText - the text currently held by the TextBox
	 */
	public String getCurrentText()
	{
		return currentText;
	}
	
	/**
	 * Sets the text currently held by this text box.
	 * The state of the text displayed in the text box will be altered
	 *  based on whether the given text is empty.
	 * If the text is empty and the text box does not have focus,
	 *  the text box displays the default text in gray;
	 *  otherwise it displays the given text in black.
	 * 
	 * @param currentText - the text currently held by the TextBox
	 */
	public void setCurrentText(String currentText)
	{
		if ((currentText == null || currentText.isEmpty()) && !hasFocus)
		{
			super.setText(defaultText);
			this.setForeground(Color.gray);
		}
		else
		{
			super.setText(currentText);
			this.setForeground(Color.black);
		}
		this.currentText = currentText;
	}
	
	/**
	 * Invoked when focus is gained by this TextBox.
	 * The text held by this TextBox is displayed in black.
	 */
	public void focusGained(FocusEvent e)
	{
		hasFocus = true;
		super.setText(currentText);
		this.setForeground(Color.black);
	}
	
	/**
	 * Invoked when focus is lost by this TextBox.
	 * If the text held by the TextBox is empty,
	 *  the default text is displayed in gray.
	 */
	public void focusLost(FocusEvent e)
	{
		hasFocus = false;
		if (currentText.isEmpty())
		{
			super.setText(defaultText);
			this.setForeground(Color.gray);
		}
	}
	
	/**
	 * Sets the text currently held by this TextBox and adjusts the current display of text likewise.
	 */
	public void setText(String text)
	{
		super.setText(text);
		
		if (text != null)
		{
			currentText = text;
		}
		else
		{
			currentText = "";
		}
		
		if (hasFocus)
		{
			this.setForeground(Color.black);
		}
		else
		{
			if (currentText.isEmpty())
			{
				super.setText(defaultText);
				this.setForeground(Color.gray);
			}
			else
			{
				this.setForeground(Color.black);
			}
		}
	}
	
	/**
	 * Invoked when a key is pressed in the TextBox.
	 * Adjusts the current text held by the TextBox.
	 */
	public void keyPressed(KeyEvent arg0)
	{
		currentText = getText();
	}
	
	/**
	 * Invoked when a key is released in the TextBox.
	 * Adjusts the current text held by the TextBox.
	 */
	public void keyReleased(KeyEvent arg0)
	{
		currentText = getText();
	}
	
	/**
	 * Invoked when a key is typed in the TextBox.
	 * Adjusts the current text held by the TextBox.
	 */
	public void keyTyped(KeyEvent arg0)
	{
		currentText = getText();
	}
}
