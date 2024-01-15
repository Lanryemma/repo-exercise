import logo from './logo.svg';
import './App.css';
import { useTheme,ThemeProvider } from './ContextApi';
import { FormApp } from './UseStateForm';
import { NewApp } from './Assignment';
import { EffectApp } from './Useeffect';
import { DataApp, App2 } from './FetchingData';


const Switch = () => {
  const { theme, toggleTheme } = useTheme();
  return (
    <label className="switch">
      <input
        type="checkbox"
        checked={theme === "light"}
        onChange={toggleTheme}
        id="toggle" class="toggle-input"
      />
      <label for="toggle" class="toggle-label"></label>
    </label>
  );
 };
 
 const Title = ({ children }) => {
  const { theme } = useTheme();
  return (
    <h2
      style={{
        color: theme === "light" ? "black" : "white",
      }}
    >
      {children}
    </h2>
  );
};

const Paragraph = ({ children }) => {
  const { theme } = useTheme();
  return (
    <p
      style={{
        color: theme === "light" ? "black" : "white",
      }}
    >
      {children}
    </p>
  );
};

const Content = () => {
  return (
    <div>
      <Paragraph>
        We are a pizza loving family. And for years, I searched and searched and
        searched for the perfect pizza dough recipe. I tried dozens, or more.
        And while some were good, none of them were that recipe that would
        make me stop trying all of the others.
      </Paragraph>
    </div>
  );
};

const Header = () => {
  return (
    <header>
      <Title>Little Lemon 🍕</Title>
      <Switch />
    </header>
  );
};

const Page = () => {
  return (
    <div className="Page">
      <Title>When it comes to dough</Title>
      <Content />
    </div>
  );
};
const Appp = ()=>{
  const { theme } = useTheme();
  return (
    <div
      className="App"
      style={{
        backgroundColor: theme === "light" ? "white" : "black",
      }}
    >
      <Header />
      <Page />
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <ThemeProvider>
        <Appp />
      </ThemeProvider>
      <FormApp/>
      <NewApp/>
      <EffectApp/>
      <DataApp/>
      <App2/>
    </div>
  );
}

export default App;
