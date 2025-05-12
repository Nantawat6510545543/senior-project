import React from "react";
import { Link } from "react-router-dom";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
} from "@/components/ui/navigation-menu";

const Navbar: React.FC = () => {
  return (
    <nav className="bg-major text-minor border-b px-6 py-4 flex items-center justify-between">
      <div className="text-xl font-semibold">SSL-MI-EEG</div>
      <NavigationMenu>
        <NavigationMenuList className="flex space-x-4">
          <NavigationMenuItem>
            <Link to="/train" className="text-sm font-medium hover:underline text-minor">
              <NavigationMenuLink>Train</NavigationMenuLink>
            </Link>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <Link to="/predict" className="text-sm font-medium hover:underline text-minor">
              <NavigationMenuLink>Predict</NavigationMenuLink>
            </Link>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <Link to="/evaluate" className="text-sm font-medium hover:underline text-minor">
              <NavigationMenuLink>Evaluate</NavigationMenuLink>
            </Link>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <Link to="/compare" className="text-sm font-medium hover:underline text-minor">
              <NavigationMenuLink>Compare Model</NavigationMenuLink>
            </Link>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
    </nav>
  );
};

export default Navbar;
