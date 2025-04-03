"use client";

import { ThemeProvider } from "next-themes";
import Navbar from "@/components/shared/navbar/Navbar";
import React from "react";
import LeftNavbar from "@/components/shared/navbar/LeftNavbar";

interface LayoutProps {
	children: React.ReactNode;
}

export default function RootLayout({ children }: LayoutProps) {
	return (
		<ThemeProvider attribute="class">
			<main className="bg-baby_veryBlack relative">
				<Navbar />
				<div className="flex">
				<LeftNavbar/>
					<section className="flex min-h-screen flex-1 flex-col px-4 pb-6 pt-24 sm:px-6 lg:px-8 lg:pt-32">
						{children}
					</section>
					{/* Placeholder right Navbar component */}
					<div className="hidden text-xl dark:text-pumpkin md:block">
						Right Navbar
					</div>
				</div>
			</main>
		</ThemeProvider>
	);
}
