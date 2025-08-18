import { useEffect, useRef, useState, type MouseEventHandler } from "react";

import GroupContainer from "./GroupContainer";
import { useManualForm } from "../../contexts/ManualFormContext";

import ProgressBar from "../ProgressBar";
import { FormGroup, ArrayFormGroup } from "./FormGroup";

const DynamicForm = () => {
    const { model, formData } = useManualForm();
    console.log({ model });
    console.log({ formData });
    const [activeTab, setActiveTab] = useState(1);

    const activeTabRef = useRef(activeTab);

    useEffect(() => {
        activeTabRef.current = activeTab;
    }, [activeTab])

    const lastTab = model.length;

    useEffect(() => {
        document.addEventListener("keydown", handleKeyDown);

        return () => document.removeEventListener("keydown", handleKeyDown);
    }, [lastTab]);

    const progress = (model.length > 1) ? Math.ceil(activeTab / model.length * 100) : 0;

    const handleKeyDown = (e: KeyboardEvent) => {
        let tab = activeTabRef.current;
        if (e.ctrlKey && e.key === "ArrowRight") {
            tab = Math.min(activeTabRef.current + 1, lastTab);
        } else if (e.ctrlKey && e.key === "ArrowLeft") {
            tab = Math.max(activeTabRef.current - 1, 1);
        }

        setActiveTab(tab);
    }

    return (
        <form className="relative flex flex-col gap-8 bg-white text-black max-w-96 w-full min-w-60 px-6 py-8 rounded-2xl shadow-2xl">
            <ProgressBar progress={progress} containerClass="absolute top-0 left-0 w-full h-1 bg-gray-200 rounded" className={`h-1 bg-black rounded transition-all`} />

            {model.map((group, index) => {
                if (activeTab - 1 === index)
                    if (group.kind === "group") {
                        return (
                            <GroupContainer key={group.key} title={group.label}>
                                <FormGroup group={group} formData={formData} />
                            </GroupContainer>
                        )
                    } else { // group.kind === 'array'
                        return (
                            <GroupContainer key={group.key} title={group.label} actions={<AddButtonGroup groupKey={group.key} />}>
                                <ArrayFormGroup group={group} formData={formData} />
                            </GroupContainer>
                        );
                    }
            }
            )}

            {
                model.length > 1 && (
                    <div className="flex justify-between items-center">
                        <TabButton
                            onClick={() => setActiveTab((prev) => prev - 1)}
                            disabled={activeTab === 1}
                        >
                            <span>Prev</span>
                        </TabButton>
                        <TabButton
                            onClick={() => setActiveTab((prev) => prev + 1)}
                            disabled={activeTab == model.length}
                        >
                            <span>Next</span>
                        </TabButton>
                    </div>
                )
            }

            <button
                type="submit"
                className="px-4 py-2 bg-black text-white rounded-lg cursor-pointer"
            >
                Submit
            </button>
        </form>
    );
};

export default DynamicForm;


interface TabButtonProps {
    title?: string;
    className?: string;
    disabled?: boolean;
    onClick: MouseEventHandler<HTMLButtonElement>;
    children: React.ReactElement;
}

const TabButton = ({ title, className, disabled, onClick, children }: TabButtonProps) => {
    return (
        <button
            type="button"
            title={title}
            className={`px-3 py-2 text-sm bg-black text-white rounded cursor-pointer disabled:cursor-default disabled:bg-gray-600 ${className}`}
            onClick={onClick}
            disabled={disabled}
        >
            {children}
        </button>
    );
};


const AddButtonGroup = ({ groupKey }: { groupKey: string }) => {
    const { addGroup } = useManualForm();

    return (
        <button type="button" className="px-4 py-2 text-xs bg-black text-white rounded-lg cursor-pointer" onClick={() => addGroup(groupKey)}>
            Add Group
        </button>
    )
}