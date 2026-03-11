from sqlalchemy import Integer, String, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./countries.db"
# The engine responsible for managing the connection to the SQLite database
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

# Defining the Country table schema
class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    clue1: Mapped[str] = mapped_column(String, nullable=False)
    clue2: Mapped[str] = mapped_column(String, nullable=False)
    clue3: Mapped[str] = mapped_column(String, nullable=False)


SEED_DATA = [
    Country(
        name="Japan",
        clue1="Bowing is a standard greeting, and removing shoes is required when entering homes.",
        clue2="It features the world's busiest pedestrian crossing in its capital city.",
        clue3="Cherry blossoms are a celebrated symbol of this country's culture.",
    ),
    Country(
        name="Brazil",
        clue1="This country contains the majority of the Amazon Rainforest.",
        clue2="It has won the FIFA World Cup a record five times.",
        clue3="It has more than 400 public airports.",
    ),
    Country(
        name="Italy",
        clue1="This country is shaped like a boot.",
        clue2="It is home to the Colosseum and the Vatican City.",
        clue3="It gave the world pizza, pasta, and the Renaissance.",
    ),
    Country(
        name="Israel",
        clue1="Contains the lowest point on Earth surface.",
        clue2="Known as the 'Start-up Nation'.",
        clue3="It has won more Nobel Prizes than all other Middle East countries combined.",
    ),
    Country(
        name="Canada",
        clue1="This country is the second largest in the world by total area.",
        clue2="It shares the world's longest international border with its southern neighbor.",
        clue3="The maple leaf is the central symbol on its national flag.",
    ),
    Country(
        name="Australia",
        clue1="Contains the world's largest sand island.",
        clue2="It is home to the Great Barrier Reef, the world's largest coral reef system.",
        clue3="It features several natural pink lakes.",
    ),
    Country(
        name="Mexico",
        clue1="This country is home to ancient Mayan and Aztec civilizations.",
        clue2="It is the world's largest producer of avocados.",
        clue3="The Day of the Dead is one of its most iconic cultural celebrations.",
    ),
]


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        count = await session.scalar(select(func.count()).select_from(Country))
        if count == 0:
            session.add_all(SEED_DATA)
            await session.commit()


async def get_random_country(session: AsyncSession) -> Country | None:
    result = await session.scalar(
        select(Country).order_by(func.random()).limit(1)
    )
    return result
