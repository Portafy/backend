import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ManualFormContextProvider } from "./contexts/ManualFormContext";
import ManualForm from "./pages/ManualForm";

function App() {
    return (
        <Router>
            <ManualFormContextProvider>
                <Routes>
                    <Route path="/manual" element={<ManualForm />} />
                </Routes>
            </ManualFormContextProvider>
        </Router>
    );
}

export default App;