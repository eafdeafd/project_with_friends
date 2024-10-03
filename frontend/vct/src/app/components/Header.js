import React from 'react';
import Link from 'next/link';

export default function Header({ title, buttons }) {
    return (
        <header className="header-container text-white p-4 flex justify-between items-center">
            <h1 className="header-title">
                <a href="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                    {title}
                </a>
            </h1>
            <nav className="header-nav flex-1 flex justify-center">
                <ul className="flex space-x-6">
                    {buttons.map((button, index) => (
                        <li key={index}>
                            <button
                                onClick={button.onClick}
                                className="nav-button text-white bg-transparent hover:text-red-500 hover:bg-gray-200 transition-colors duration-200 ease-in-out px-2 py-1 rounded"
                            >
                                {button.label}
                            </button>
                        </li>
                    ))}
                </ul>
            </nav>
            <Link
                href="https://login.playvalorant.com/"
                className="play-now-button bg-red-600 hover:bg-white hover:text-black text-white font-bold py-2 px-4 rounded transition-colors duration-200 ease-in-out"
            >
                PLAY NOW
            </Link>
        </header>
    );
}