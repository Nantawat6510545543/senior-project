import React from "react";
import { NavLink } from "react-router-dom";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
} from "@/components/ui/navigation-menu";

const navItems = [
  { to: "/eegui", label: "EEGUI" },
  { to: "/train", label: "Train" },
  { to: "/predict", label: "Predict" },
  { to: "/evaluate", label: "Evaluate" },
  { to: "/compare", label: "Compare Model" },
];

const Navbar: React.FC = () => {
  return (
    <div>
      <nav className="fixed top-0 left-0 right-0 z-50 bg-purple-800 text-white px-6 py-4 flex items-center justify-between">
        <div className="text-2xl font-bold">SSL-MI-EEG</div>
        <NavigationMenu>
          <NavigationMenuList className="flex space-x-4">
            {navItems.map((item) => (
              <NavigationMenuItem key={item.to}>
                <NavLink
                  to={item.to}
                  className={({ isActive }) =>
                    isActive
                      ? "bg-purple-100 text-purple-800 text-lg px-4 py-2 rounded-lg" // Active state
                      : "bg-transparent text-white px-4 text-lg py-2 rounded-lg" // Default state
                  }
                >
                  {item.label}
                </NavLink>
              </NavigationMenuItem>
            ))}
          </NavigationMenuList>
        </NavigationMenu>
      </nav>
      <div className="pt-16"></div>
    </div>
  );
};

export default Navbar;
