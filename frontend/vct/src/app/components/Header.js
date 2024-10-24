import React from 'react';
import Link from 'next/link';
import { Users } from 'lucide-react';

export default function Header({ title, buttons }) {
    return (
        <header className="header-container text-white p-4 flex justify-between items-center">
            <div className="icon-padding"><Users className="w-4 h-4 text-white group-hover:text-black transition-colors duration-200 ease-in-out"></Users></div>
            <h1 className="header-title">
                <a href="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                    {title}
                </a>
            </h1>
            <nav className="header-nav flex-1 flex justify-center header-centering">
                <ul className="flex space-x-6">
                    {buttons.map((button, index) => (
                        <li key={index}>
                            <button
                                onClick={() => window.open(button.link, '_blank')}
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
                target="_blank" 
                rel="noopener noreferrer" 
                className="play-now-button bg-red-600 hover:bg-white hover:text-black text-white font-bold py-2 px-4 rounded transition-colors duration-200 ease-in-out"
            >
                PLAY NOW
            </Link>
        </header>
    );
}