
package laab1;
public class Laab1 {

    public static void main(String[] args) 
    {
        //MY TEST:
        String []de={"de"};
        String []k={"oil","prove","g","try","d","orange","g","game"};
        WordList j= new WordList(k);
        //test case #0: insert() to a 1 word list with a word already in list
        System.out.println("test case #0: insert() to a 1 word list with a word already in list");
        WordList dee= new WordList(de);
        dee.insert("de");
        System.out.println(dee.toString());
        //test case #1: getWordAt(i) for a non empty list  
        System.out.println("test #1: getWordAt() for a non empty list");
        System.out.println(j.getWordAt(0));
        try{
            System.out.println(j.getWordAt(-1));
        }
        catch(ArrayIndexOutOfBoundsException e){System.out.println(e);}
        
        System.out.println(j.getWordAt(4));
        try{ 
            System.out.println(j.getWordAt(7));
            
        }
        catch(ArrayIndexOutOfBoundsException e){System.out.println(e);}
       
        //test case #2: insert() in middle of non empty list
        System.out.println("test #2: insert() in middle of non empty list");
        j.insert("hi");
        System.out.println(j.toString());
        System.out.println(j.getSize());
        System.out.println(j.getCapacity());
        //test case #3: insert() for a list that already contains the word
        System.out.println("test case #3: insert() for a list that already contains the word");
        j.insert("try");
        System.out.println(j.toString());
        System.out.println(j.getSize());
        System.out.println(j.getCapacity());
        //test case #4: insert() at the beginning of a non empty list 
        System.out.println("test case #4: insert() at the beginning of a non empty list ");
        j.insert("alex");
        System.out.println(j.toString());
        System.out.println(j.getSize());
        System.out.println(j.getCapacity());
        //test case #5: insert() at the end of a non empty list 
        System.out.println("test case #5: insert() at the end of a non empty list ");
        j.insert("z");
        System.out.println(j.toString());
        System.out.println(j.getSize());
        System.out.println(j.getCapacity());
         //test case #6: insert() for an empty list
        WordList n= new WordList(5);
        System.out.println("test case #6: insert() for an empty list");
        n.insert("s");
        System.out.println(n.toString());
        System.out.println(n.getSize());
        System.out.println(n.getCapacity());
        n.insert("bee");
        System.out.println(n.toString());
        System.out.println(n.getSize());
        System.out.println(n.getCapacity());
        //test case #7: find() a word in the list
        System.out.println("test case #7: find() a word in the list");
        int indexx=0;
        indexx=j.find("hi");
        System.out.println(indexx);
        //test case #8: find() a word not in the list
        System.out.println("test case #8: find() a word not in the list");
        indexx=j.find("blarg");
        System.out.println(indexx);
        //test case #9: remove() a word in the list
        System.out.println("test case #9: remove() a word in the list");
        j.remove("z");
        System.out.println(j.toString());
        System.out.println(j.getSize());
        System.out.println(j.getCapacity());
         //test case #10: remove() a word not in the list
        System.out.println("test case #10: remove() a word not in the list");
        j.remove("z");
        System.out.println(j.toString());
        System.out.println(j.getSize());
        System.out.println(j.getCapacity());
        //test case #11: sublist() creating a non empty list
        System.out.println("test case #11: Wordlist() creating a non empty list");
        WordList u=j.sublist('d', 'p');
        System.out.println(u.toString());
        System.out.println(u.getSize());
        System.out.println(u.getCapacity());
        //test case #12: sublist() creating an empty list
        System.out.println("test case #12: Wordlist() creating an empty list");
        WordList f=j.sublist('y', 'z');
        System.out.println(f.toString());
        System.out.println(f.getSize());
        System.out.println(f.getCapacity());
        //test case #13: sublist() creating a list with only 1 word (end)
        System.out.println("test case #13: sublist() creating a list with only 1 word (end)");
        WordList tx=j.sublist('t', 'z');
        System.out.println(tx.toString());
        System.out.println(tx.getSize());
        System.out.println(tx.getCapacity());
       //test case #14: sublist() creating a list with only 1 word (beginning)
        System.out.println("test case #14: sublist() creating a list with only 1 word (beginning)");
        WordList nx=j.sublist('a', 'b');
        System.out.println(nx.toString());
        System.out.println(nx.getSize());
        System.out.println(nx.getCapacity());
        //test case #15: remove() a word not in the list (empty list)
        System.out.println("test case #15: remove() a word not in the list (empty list)");
        WordList fg=new WordList(4);
        fg.remove("pie");
        System.out.println(fg.toString());
        System.out.println(fg.getSize());
        System.out.println(fg.getCapacity());
        //test case #16: getWordAt() for an empty list
        System.out.println("test case #16: getWordAt() for an empty list");
         try{
            System.out.println(fg.getWordAt(3));
        }
        catch(ArrayIndexOutOfBoundsException e){System.out.println(e);}
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    }
}
