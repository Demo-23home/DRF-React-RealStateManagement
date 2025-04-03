"use client";

import { Button } from "@/components/ui/button";
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { MoonIcon, SunIcon } from "@radix-ui/react-icons";
import { useTheme } from "next-themes";

const themeOptions = [
	{ value: "light", label: "Light" },
	{ value: "dark", label: "Dark" },
	{ value: "system", label: "System" },
];

export default function ThemeSwitcher() {
	const { theme, setTheme, resolvedTheme } = useTheme();

	return (
		<div className="flex items-center gap-2">
			<DropdownMenu>
				<DropdownMenuTrigger asChild>
					<Button
						size="icon"
						className="relative flex items-center justify-center border-none bg-transparent p-0 shadow-none hover:bg-transparent"
					>
						{/* Sun icon (shown in light mode) */}
						<SunIcon
							className={`absolute size-6 transition-all ${
								resolvedTheme === "light"
									? "text-pumpkin opacity-100"
									: "opacity-0"
							}`}
						/>
						{/* Moon icon (shown in dark mode) */}
						<MoonIcon
							className={`absolute size-6 transition-all ${
								resolvedTheme === "dark"
									? "text-blue-400 opacity-100"
									: "opacity-0"
							}`}
						/>
						<span className="sr-only">Toggle theme</span>
					</Button>
				</DropdownMenuTrigger>

				<DropdownMenuContent
					align="end"
					className="rounded-md bg-white p-2 dark:bg-black"
				>
					{themeOptions.map(({ value, label }) => (
						<DropdownMenuItem
							key={value}
							onClick={() => setTheme(value)}
							className={`cursor-pointer ${
								resolvedTheme === value
									? "text-blue-500"
									: "text-gray-700 dark:text-gray-300"
							}`}
						>
							{label}
						</DropdownMenuItem>
					))}
				</DropdownMenuContent>
			</DropdownMenu>
		</div>
	);
}
