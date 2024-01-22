import logo from './logo.svg';
import './App.css';
import { HigherOrderDisplay } from './HigherOrderComponent';
import { MouseApp } from './HigherOrderComponent';
import { RenderDisplay } from './RenderProps';
import { RenderMouseApp } from './RenderProps';

function App() {
  return (
    <div className="App">
      <HigherOrderDisplay/>
      <MouseApp/>
      <RenderDisplay/>
      <RenderMouseApp/>
    </div>
  );
}

export default App;
