//Side effect is something that makes a function impure
//impur fumctions are functions that have external element
//thta wasnt defined in the function or the parent function of the function
function MenuPage(props) { 
    const [data, setData] = useState([]); 
  
    useEffect(() => { 
      document.title = 'Little Lemon'; 
    }, []); 
  
    useEffect(() => { 
      fetch(`https://littlelemon/menu/${id}`) 
        .then(response => response.json()) 
        .then(json => setData(json)); 
    }, [props.id]); 
  
    // ... 
} 


//Effects with Cleanup
//For example, you may want to set up a subscription to an external data source. 
//In that scenario, it is vital to perform a cleanup after the effect finishes its execution. 
//If your effect returns a function, 
//React will run it when it’s time to clean up resources and free unused memory.
function LittleLemonChat(props) { 
    const [status, chatStatus] = useState('offline'); 
  
    useEffect(() => { 
      LemonChat.subscribeToMessages(props.chatId, () => setStatus('online')) 
  
      return () => { 
        setStatus('offline'); 
        LemonChat.unsubscribeFromMessages(props.chatId); 
      }; 
    }, []); 
  
    // ... 
} 