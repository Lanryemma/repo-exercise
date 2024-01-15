//After that little adjustment, you will prevent any rendering from happening in all ComponentA, 
//ComponentB and ComponentC if the App component re-renders
const App = () => {
    return (
       <AppContext.Provider>
         <ComponentA />
       </AppContext.Provider>
     );
    };
    
    const ComponentA = React.memo(() => <ComponentB />);
    const ComponentB = () => <ComponentC />;
    const ComponentC = () => null;


// ComponentC is now a consumer of context, 
//so any time the provider value prop changes, ComponentC will re-render.
const App1 = () => {
      const value = {a: 'hi', b: 'bye'};
      return (
        <AppContext.Provider value={value}>
          <ComponentA1 />
        </AppContext.Provider>
      );
    };
    
    const ComponentA1 = React.memo(() => <ComponentB1 />);
    const ComponentB1 = () => <ComponentC1 />;
    const ComponentC1 = () => {
      const contextValue = useContext(AppContext);
      return null;
    };
    //the sequence of re-renders would be:(App (ContextProvider) -> C)



//Imagine that the value prop from the provider changes to {a: ‘hello’, b: ‘bye’} and then back to {a: 'hi', b: 'bye'}
//Even though the provider value doesn’t seem to change, ComponentC gets re-rendered.
//That is because object comparison in JavaScript is done by reference. 
//Every time a new re-render happens in the App component, a new instance of the value object is created
//This problem can be resolved by using the 'useMemo' hook from React as follows.
const App2 = () => {
      const a = 'hi';
      const b = 'bye';
      const value = useMemo(() => ({a, b}), [a, b]);
    
      return (
        <AppContext.Provider value={value}>
          <ComponentA2 />
        </AppContext.Provider>
      );
    };
    
    const ComponentA2 = React.memo(() => <ComponentB2 />);
    const ComponentB2 = () => <ComponentC2 />;
    const ComponentC2 = () => {
      const contextValue = useContext(AppContext);
      return null;
    };