import React from "react";
import { NavLink } from "react-router-dom";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
} from "@/components/ui/navigation-menu";

const navItems = [
  { to: "/train", label: "Train" },
  { to: "/predict", label: "Predict" },
  { to: "/evaluate", label: "Evaluate" },
  { to: "/compare", label: "Compare Model" },
];

const Navbar: React.FC = () => {
  return (
    <nav className="bg-major text-minor border-b px-6 py-4 flex items-center justify-between">
      <div className="text-xl font-semibold">SSL-MI-EEG</div>
      <NavigationMenu>
        <NavigationMenuList className="flex space-x-4">
          {navItems.map((item) => (
            <NavigationMenuItem key={item.to}>
              <NavLink to={item.to}>
                <NavigationMenuLink>{item.label}</NavigationMenuLink>
              </NavLink>
            </NavigationMenuItem>
          ))}
        </NavigationMenuList>
      </NavigationMenu>
    </nav>
  );
};

export default Navbar;
