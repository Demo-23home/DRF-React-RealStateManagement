"use client";
import { Button } from "@/components/ui/button";
import {
	Sheet,
	SheetClose,
	SheetContent,
	SheetFooter,
	SheetTrigger,
} from "@/components/ui/sheet";
import { leftNavLinks } from "@/constants";
import { HomeModernIcon } from "@heroicons/react/24/solid";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";

function LeftNavContent() {
	const pathname = usePathname();

	return (
		<section className="flex h-full flex-col gap-6 pt-16">
			{leftNavLinks.map((linkItem) => {
				const isActive =
					(pathname.includes(linkItem.path) && linkItem.path.length > 1) ||
					pathname === linkItem.path;
				return (
					<SheetClose asChild key={linkItem.path}>
						<Link
							href={linkItem.path}
							className={`${isActive ? "electricIndigo-gradient rounded-lg text-babyPowder" : "text-baby_richBlack"} flex items-center justify-start gap-4 bg-transparent p-4`}
						>
							<Image
								src={linkItem.imgLocation}
								alt={linkItem.label}
								width={22}
								height={22}
								className={`${isActive ? "" : "color-invert"}`}
							/>
							<p className={`${isActive ? "base-bold" : "base-medium"}`}>
								{linkItem.label}
							</p>
						</Link>
					</SheetClose>
				);
			})}
		</section>
	);
}

export default function MobileNavbar() {
	return (
		<Sheet>
			<SheetTrigger asChild>
				<Image
					src="/assets/icons/mobile-menu.svg"
					alt="Mobile Menu"
					width={36}
					height={36}
					className="invert-colors cursor-pointer sm:hidden"
				/>
			</SheetTrigger>
			{/* Fix: Add flex column layout with full height */}
			<SheetContent
				side="left"
				className="bg-baby_rich flex h-full flex-col border-none"
			>
				{/* Header Section */}
				<Link href="/" className="flex items-center gap-1">
					<HomeModernIcon className="mr-2 size-11 text-lime-500" />
					<p className="h2-bold text-baby_veryBlack font-robotoSlab">
						Alpha <span className="text-lime-500">Apartments</span>
					</p>
				</Link>

				{/* Fix: Wrap LeftNavContent inside a div that takes remaining space */}
				<div className="grow overflow-y-auto">
					<LeftNavContent />
				</div>

				{/* Footer Section - Stays at the bottom */}
				<SheetFooter className="border-gray-300 dark:border-gray-700 flex flex-col gap-3 border-t p-4">
					<SheetClose asChild>
						<Link href="/register">
							<Button className="electricIndigo-gradient small-medium light-border-2 btn-tertiary mt-4 min-h-[41px] w-full rounded-lg border px-4 py-3 text-babyPowder shadow-none">
								Register
							</Button>
						</Link>
					</SheetClose>

					<SheetClose asChild>
						<Link href="/login">
							<Button className="lime-gradient small-medium light-border-2 btn-tertiary min-h-[41px] w-full rounded-lg border px-4 py-3 text-babyPowder shadow-none">
								Login
							</Button>
						</Link>
					</SheetClose>
				</SheetFooter>
			</SheetContent>
		</Sheet>
	);
}
