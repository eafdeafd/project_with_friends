import React from 'react';

export default function Header({ title, buttons }) {
    return (
        <div className="header-container">
            <h1 className="header-title">{title}</h1>
            <div className="button-container">
                {buttons.map((button, index) => (
                    <button
                        key={index}
                        className="info-button"
                        onClick={button.onClick}
                    >
                        {button.label}
                    </button>
                ))}
            </div>
        </div>
    );
}
