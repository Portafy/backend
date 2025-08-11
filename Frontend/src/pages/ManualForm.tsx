import type { InputChangeEventType } from "../utils/types";
import { useState } from "react";

import { FormGroup } from "../components/forms/FormGroup";

import { buildFormGroups, flattenFields } from "../utils/formBuilder";

import jsonTemplate from "../utils/data_format.json";

const ManualForm = () => {
    const formGroupsArray = buildFormGroups(jsonTemplate);
    const [manualData, setManualData] = useState(
        flattenFields(formGroupsArray)
    );
    console.log("formGroupsArray: ", formGroupsArray)
    console.log("manualData: ", manualData)
    const [formTab, setFormTab] = useState<number>(0);

    const handleChange = (e: InputChangeEventType ) => {
        const { name, value } = e.target;
        setManualData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    return (
        <main className="flex flex-col justify-center gap-8 items-center p-12 w-full min-h-screen">
            <form className="flex flex-col gap-8 bg-black text-white max-w-96 w-full min-w-60 px-6 py-8 rounded-2xl shadow-2xl">
                <div className="flex">
                    {formGroupsArray.map((group, index) => {
                        if (index === formTab)
                            return (
                                <FormGroup
                                    key={index}
                                    group={group}
                                    data={manualData}
                                    onChange={handleChange}
                                />
                            );
                    })}
                </div>

                <div className="flex justify-between items-center">
                    <button
                        type="button"
                        className="px-4 py-2 bg-white text-black rounded-lg cursor-pointer disabled:cursor-default disabled:bg-gray-600"
                        onClick={() => setFormTab((prev) => prev - 1)}
                        disabled={formTab === 0}
                    >
                        Previous
                    </button>
                    <button
                        type="button"
                        className="px-4 py-2 bg-white text-black rounded-lg cursor-pointer disabled:cursor-default disabled:bg-gray-600"
                        onClick={() => setFormTab((prev) => prev + 1)}
                        disabled = {formTab == formGroupsArray.length - 1}
                    >
                        Next
                    </button>
                </div>
            </form>
            {true && (
                <button
                    type="submit"
                    className="px-4 py-2 bg-black text-white rounded-lg cursor-pointer"
                >
                    Submit
                </button>
            )}
        </main>
    );
};

export default ManualForm;
