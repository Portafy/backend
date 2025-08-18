import { useEffect } from "react";

import DynamicForm from "../components/forms/DynamicForm";
import { useManualForm } from "../contexts/ManualFormContext";
import { useLocation } from "react-router-dom";

import sample_data from "../seed/sample_data.json"

const ManualForm = () => {
    const { populate } = useManualForm();
    const location = useLocation()
    const searchParams = new URLSearchParams(location.search)

    useEffect(() => {
        if (searchParams.has("recheck")) {
            populate(sample_data);
        }
    }, [])

    return (
        <main className="flex flex-col justify-center items-center min-h-screen gap-8 p-6 w-full">
            <DynamicForm />
        </main>
    );
};

export default ManualForm;