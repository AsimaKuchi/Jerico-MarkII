import { useNavigate, useLocation } from "react-router-dom";
import { API } from "@/App";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  LayoutDashboard,
  Search,
  User,
  FileText,
  MessageSquare,
  LogOut,
  Menu,
  X,
  Home,
} from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

const navItems = [
  { icon: LayoutDashboard, label: "Dashboard", path: "/dashboard" },
  { icon: Search, label: "Find Jobs", path: "/jobs" },
  { icon: FileText, label: "Applications", path: "/applications" },
  { icon: MessageSquare, label: "Interview Prep", path: "/interview-prep" },
  { icon: User, label: "Profile", path: "/profile" },
  { icon: Home, label: "Back to Home", path: "/" },
];

export const Navbar = ({ user }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = async () => {
    try {
      await fetch(`${API}/auth/logout`, {
        method: "POST",
        credentials: "include",
      });
      navigate("/", { replace: true });
      toast.success("Logged out successfully");
    } catch (error) {
      navigate("/", { replace: true });
    }
  };

  const isActive = (path) => location.pathname === path;

  const NavList = ({ onNavigate }) => (
    <nav className="flex flex-col gap-1">
      {navItems.map((item) => {
        const active = isActive(item.path);
        return (
          <button
            key={item.path}
            data-testid={`nav-${item.label.toLowerCase().replace(/\s/g, "-")}`}
            onClick={() => {
              navigate(item.path);
              onNavigate?.();
            }}
            className={`group flex items-center gap-3 px-4 py-3 border-l-2 font-mono text-xs uppercase tracking-widest transition-colors duration-200 ${
              active
                ? "border-primary text-primary bg-white/5"
                : "border-transparent text-sidebar-muted hover:text-sidebar-foreground hover:border-sidebar-muted"
            }`}
          >
            <item.icon className="w-4 h-4 shrink-0" />
            <span>{item.label}</span>
          </button>
        );
      })}
    </nav>
  );

  const UserMenu = () => (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button
          className="flex items-center gap-3 w-full px-4 py-3 border border-sidebar-border hover:border-sidebar-muted transition-colors"
          data-testid="user-menu-trigger"
        >
          <Avatar className="h-8 w-8 rounded-none">
            <AvatarImage src={user?.picture} alt={user?.name} />
            <AvatarFallback className="bg-primary text-primary-foreground rounded-none font-mono">
              {user?.name?.charAt(0) || "U"}
            </AvatarFallback>
          </Avatar>
          <div className="text-left min-w-0">
            <p className="text-xs font-semibold text-sidebar-foreground truncate max-w-[120px]">
              {user?.name?.split(" ")[0] || "Account"}
            </p>
            <p className="text-[10px] font-mono text-sidebar-muted truncate max-w-[120px]">
              {user?.email}
            </p>
          </div>
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start" side="top" className="w-56 bg-popover border border-border rounded-none">
        <div className="px-3 py-2">
          <p className="text-sm font-semibold text-foreground">{user?.name}</p>
          <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
        </div>
        <DropdownMenuSeparator className="bg-border" />
        <DropdownMenuItem onClick={() => navigate("/profile")} className="cursor-pointer rounded-none font-mono text-xs uppercase tracking-wider">
          <User className="w-4 h-4 mr-2" />
          Profile Settings
        </DropdownMenuItem>
        <DropdownMenuSeparator className="bg-border" />
        <DropdownMenuItem
          data-testid="logout-btn"
          onClick={handleLogout}
          className="cursor-pointer rounded-none font-mono text-xs uppercase tracking-wider text-destructive focus:text-destructive"
        >
          <LogOut className="w-4 h-4 mr-2" />
          Log out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );

  return (
    <>
      {/* Desktop sidebar */}
      <aside
        className="hidden md:flex fixed top-0 left-0 z-50 h-screen w-64 flex-col bg-sidebar border-r border-sidebar-border"
        data-testid="navbar"
      >
        <div
          className="flex items-center gap-3 px-6 h-20 border-b border-sidebar-border cursor-pointer"
          onClick={() => navigate("/dashboard")}
        >
          <div className="w-9 h-9 bg-primary flex items-center justify-center">
            <span className="font-mono font-bold text-primary-foreground text-lg">J</span>
          </div>
          <span className="text-xl font-serif font-bold text-sidebar-foreground">JobMatch AI</span>
        </div>
        <div className="flex-1 overflow-y-auto py-6">
          <p className="micro-label text-sidebar-muted px-6 mb-3">Navigation</p>
          <NavList />
        </div>
        <div className="p-4 border-t border-sidebar-border">
          <UserMenu />
        </div>
      </aside>

      {/* Mobile top bar */}
      <header className="md:hidden sticky top-0 z-50 bg-sidebar border-b border-sidebar-border" data-testid="navbar-mobile">
        <div className="flex items-center justify-between h-16 px-4">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate("/dashboard")}>
            <div className="w-8 h-8 bg-primary flex items-center justify-center">
              <span className="font-mono font-bold text-primary-foreground">J</span>
            </div>
            <span className="text-lg font-serif font-bold text-sidebar-foreground">JobMatch AI</span>
          </div>
          <button
            className="text-sidebar-foreground p-2"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            data-testid="mobile-menu-toggle"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
        {mobileMenuOpen && (
          <div className="border-t border-sidebar-border py-4 px-2">
            <NavList onNavigate={() => setMobileMenuOpen(false)} />
            <div className="p-2 mt-2">
              <UserMenu />
            </div>
          </div>
        )}
      </header>
    </>
  );
};

export default Navbar;
